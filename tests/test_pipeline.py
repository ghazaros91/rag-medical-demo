import pytest
from chunking import DocumentChunker
from rag import RAGRetriever
from pipeline import RAGPipeline
from memory import SessionMemory

@pytest.mark.asyncio
async def test_pipeline_end_to_end():
    chunker = DocumentChunker()
    splits = chunker.split_documents(chunker.load_documents())

    rag = RAGRetriever(splits)
    rag.build()

    memory = SessionMemory()
    pipeline = RAGPipeline(rag, memory)
    pipeline.build()

    result = await pipeline.run("hello world")

    assert "answer" in result
    assert isinstance(result["answer"], str)

