import chromadb
from chromadb.config import Settings

class ChromaDBClient:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
    def get_or_create_collection(self, collection_name):
        return self.client.get_or_create_collection(name=collection_name)
    
    def add_documents(self, collection_name, documents, metadatas=None, ids=None):
        collection = self.get_or_create_collection(collection_name)
        
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
            
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
    def query_documents(self, collection_name, query_texts, n_results=5):
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
    
    def delete_collection(self, collection_name):
        self.client.delete_collection(name=collection_name)
        
    def list_collections(self):
        return self.client.list_collections()
