import gradio as gr
import asyncio
from chunking import DocumentChunker
from rag import RAGRetriever
from memory import SessionMemory
from pipeline import RAGPipeline


chunker = DocumentChunker()
docs = chunker.load_documents()
chunks = chunker.chunk_documents(docs)

rag = RAGRetriever(chunks)
rag.build()

memory = SessionMemory()
pipeline = RAGPipeline(retriever=rag, memory=memory)
pipeline.build()


async def respond_async(message, history):
    result = await pipeline.run(message)
    answer = result.get("answer", "")
    memory.add(message, answer)
    return answer

def respond(message, history):
    return asyncio.run(respond_async(message, history))

chatbot = gr.ChatInterface(
    respond,
    title="Local RAG Chat",
    description="RAG + LangGraph + OOP architecture"
)

if __name__ == "__main__":
    chatbot.launch()