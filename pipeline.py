from typing import TypedDict, List, Optional, Any
from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatOllama as OllamaChat

from streaming import Streamer
from config import MODEL_NAME
from reliability import Reliability
from rag import RAGRetriever 


class PipelineState(TypedDict, total=False):
    query: str
    docs: Optional[List[Any]]
    route: Optional[str]
    answer: Optional[str]


class RAGPipeline:
    def __init__(self, retriever: RAGRetriever, memory, streamer=None):
        self.retriever = retriever
        self.memory = memory
        self.streamer = streamer or Streamer()
        self.graph = None

    def build(self):
        async def retrieve_step(state: PipelineState) -> PipelineState:
            q = state["query"]
            docs = await self.retriever.get_relevant_documents(q) 
            state["docs"] = docs
            return state
        
        async def decide_step(state: PipelineState) -> PipelineState:
            state["route"] = "respond" if state.get("docs") else "fallback"
            return state

        async def respond_step(state: PipelineState) -> PipelineState:
            llm = OllamaChat(model=MODEL_NAME, streaming=True)

            docs_text = "\n".join(getattr(d, "page_content", str(d)) for d in state.get("docs", []))
            memory_context = self.memory.context() if self.memory else ""

            prompt = f"""
                Memory:
                {memory_context}

                Retrieved context:
                {docs_text}

                User: {state["query"]}
            """

            async def call():
                text = ""
                async for chunk in llm.astream(prompt): 
                    token = chunk.content # Get the text content from the chunk
                    self.streamer.write(token)
                    text += token
                return text

            state["answer"] = await Reliability.with_retries(call)
            return state

        async def fallback_step(state: PipelineState) -> PipelineState:
            self.streamer.write("No context found. Answering generally...\n")
            llm = OllamaChat(model=MODEL_NAME, streaming=True)

            async def call():
                text = ""
                async for chunk in llm.astream("General answer: " + state["query"]):
                    token = chunk.content
                    self.streamer.write(token)
                    text += token
                return text

            state["answer"] = await Reliability.with_retries(call)
            return state
        
        graph = StateGraph(PipelineState)
        graph.add_node("retrieve", retrieve_step)
        graph.add_node("decide", decide_step)
        graph.add_node("respond", respond_step)
        graph.add_node("fallback", fallback_step)
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "decide")
        graph.add_conditional_edges(
            "decide",
            lambda s: s["route"],
            {"respond": "respond", "fallback": "fallback"}
        )
        graph.add_edge("respond", END)
        graph.add_edge("fallback", END)
        self.graph = graph.compile()

    async def run(self, query: str):
        if self.graph is None:
            raise RuntimeError("Pipeline not built. Call build() first.")
        state: PipelineState = {"query": query}
        return await self.graph.ainvoke(state)