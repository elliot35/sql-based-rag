from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any
import os

class VectorSearch:
    def __init__(self):
        # Initialize the sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        
    def create_index(self, documents: List[Dict[str, Any]]):
        """Create FAISS index from documents."""
        # Create document texts for embedding
        texts = [
            f"{doc['title']}\n{doc['content']}\n{' '.join(doc['tags'])}"
            for doc in documents
        ]
        
        # Generate embeddings
        embeddings = self.model.encode(texts, convert_to_tensor=True)
        embeddings = embeddings.cpu().numpy()  # Convert to numpy array
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add vectors to the index
        self.index.add(embeddings.astype('float32'))
        
        # Store original documents
        self.documents = documents
        
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for most similar documents."""
        if not self.index:
            raise ValueError("Index not created. Call create_index first.")
            
        # Generate query embedding
        query_embedding = self.model.encode([query])
        query_embedding = query_embedding.reshape(1, -1)
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Get results with similarity scores
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):  # Check if index is valid
                doc = self.documents[idx].copy()
                # Convert distance to similarity score (1 / (1 + distance))
                doc['relevance_score'] = float(1 / (1 + distance))
                results.append(doc)
                
        return results 