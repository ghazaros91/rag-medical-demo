import logging
import asyncio
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.retrievers import BaseRetriever


class RAGRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.retriever: BaseRetriever = None 

    def build(self):
        try:
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            vectordb = FAISS.from_documents(self.documents, embeddings)
            self.retriever = vectordb.as_retriever(search_kwargs={"k": 4})
        except Exception as e:
            logging.error(f"Error building retriever: {e}")
            raise

    async def get_relevant_documents(self, query):
        if self.retriever is None:
             raise RuntimeError("Retriever must be built before use. Call .build() first.")

    
        return await asyncio.to_thread(
            self.retriever._get_relevant_documents, 
            query,
            run_manager=None
        )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("This file contains the RAGRetriever class and is not intended to be run directly.")