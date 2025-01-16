from openai import AsyncOpenAI
from django.conf import settings
import numpy as np
from api.models import Document
from channels.db import database_sync_to_async

class RAGService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def create_embedding(self, text: str) -> list:
        """Create an embedding vector for the given text"""
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    @database_sync_to_async
    def store_document(self, content: str, embedding: list) -> Document:
        """Store a document and its embedding"""
        return Document.objects.create(
            content=content,
            embedding=embedding
        )
    
    @database_sync_to_async
    def get_similar_documents(self, query_embedding: list, num_results: int = 3) -> list:
        """Find most similar documents using cosine similarity"""
        documents = Document.objects.all()
        if not documents:
            return []
        
        # Calculate cosine similarity for each document
        similarities = []
        for doc in documents:
            if doc.embedding:
                similarity = self._cosine_similarity(query_embedding, doc.embedding)
                similarities.append((similarity, doc))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in similarities[:num_results]]
    
    def _cosine_similarity(self, vec1: list, vec2: list) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    async def add_document(self, content: str) -> Document:
        """Add a new document with its embedding"""
        embedding = await self.create_embedding(content)
        return await self.store_document(content, embedding)
    
    async def get_relevant_context(self, query: str) -> str:
        """Get relevant context for a query"""
        query_embedding = await self.create_embedding(query)
        similar_docs = await self.get_similar_documents(query_embedding)
        # Combine content from similar documents
        context = "\n\n".join([doc.content for doc in similar_docs])
        return context if context else ""
