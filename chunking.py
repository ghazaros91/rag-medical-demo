import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import DATA_DIR

class DocumentChunker:
    def __init__(self, chunk_size=600, chunk_overlap=80):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )

    def load_documents(self):
        docs = []
        for f in DATA_DIR.iterdir():
            if f.suffix in {".md", ".txt"}:
                try:
                    content = f.read_text()
                    docs.append(Document(page_content=content, metadata={"source": f.name}))
                except Exception as e:
                    logging.error(f"Failed to load {f.name}: {e}")
        return docs

    def chunk_documents(self, docs):
        return self.splitter.split_documents(docs)
