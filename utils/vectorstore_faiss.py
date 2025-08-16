# utils/vectorstore_faiss.py

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Set environment variables to force PyTorch
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

def _get_embedding_model():
    """Returns the HuggingFace embedding model."""
    # This model is fast, free, and runs locally.
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    # Use 'cuda' if you have a GPU, otherwise 'cpu'
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def create_faiss_vectorstore(documents: list[Document], index_path: str):
    """Creates a FAISS vector store from documents and saves it locally."""
    if not documents:
        raise ValueError("No documents provided to create the vector store.")
    
    embeddings = _get_embedding_model()
    # This creates the vector store in memory from your documents
    vs = FAISS.from_documents(documents, embedding=embeddings)
    # This saves the vector store to your local disk
    vs.save_local(index_path)
    print(f"FAISS index saved to: {index_path}")
    return vs

def load_faiss_vectorstore(index_path: str):
    """Loads a FAISS vector store from a local path."""
    embeddings = _get_embedding_model()
    # `allow_dangerous_deserialization=True` is required by LangChain for FAISS
    vs = FAISS.load_local(
        index_path, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    return vs