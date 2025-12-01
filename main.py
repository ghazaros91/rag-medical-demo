import asyncio
import logging
from config import LOG_FILE
from chunking import DocumentChunker
from rag import RAGRetriever
from memory import SessionMemory
from pipeline import RAGPipeline

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

async def cli():
    chunker = DocumentChunker()
    docs = chunker.load_documents()
    chunks = chunker.chunk_documents(docs)

    rag = RAGRetriever(chunks)
    rag.build()

    memory = SessionMemory()
    pipeline = RAGPipeline(retriever=rag, memory=memory)
    pipeline.build()

    print("RAG CLI (OOP) — type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        result = await pipeline.run(query)
        answer = result.get("answer", "")
        print("\n")
        memory.add(query, answer)

if __name__ == "__main__":
    try:
        asyncio.run(cli())
    except KeyboardInterrupt:
        print("\nGoodbye.")
