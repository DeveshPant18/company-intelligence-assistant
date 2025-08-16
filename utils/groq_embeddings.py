# utils/groq_embeddings.py
import os
from langchain.embeddings.base import Embeddings
from groq import GroqClient

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqEmbeddings(Embeddings):
    """
    Wrapper for using Groq LLM embeddings with LangChain/Pinecone.
    """
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.client = GroqClient(api_key=GROQ_API_KEY)
        self.dimension = 1536  # adjust based on Groq model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_text(text)

    def embed_text(self, text: str) -> list[float]:
        """
        Returns embedding vector for a single text using Groq.
        """
        resp = self.client.embeddings(model=self.model, input=text)
        return resp["embedding"]
