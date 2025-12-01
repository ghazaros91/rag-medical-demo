import pytest
from chunking import DocumentChunker

def test_load_documents():
    chunker = DocumentChunker()
    docs = chunker.load_documents()
    assert len(docs) > 0, "Should load at least one document"
    assert all(d.metadata["source"] for d in docs)

def test_split_documents():
    chunker = DocumentChunker()
    docs = chunker.load_documents()
    splits = chunker.split_documents(docs)
    assert len(splits) >= len(docs), "Splits should be >= docs"
    assert splits[0].page_content.strip() != ""
