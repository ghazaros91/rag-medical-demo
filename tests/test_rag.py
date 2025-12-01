import pytest
from chunking import DocumentChunker
from rag import RAGRetriever

@pytest.mark.asyncio
async def test_rag_retriever():
    chunker = DocumentChunker()
    docs = chunker.split_documents(chunker.load_documents())

    rag = RAGRetriever(docs)
    rag.build()

    results = await rag.get_relevant("test")
    assert isinstance(results, list)
