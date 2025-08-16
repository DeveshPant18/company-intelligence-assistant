from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
os.environ["USE_TF"] = "0"  # disable TensorFlow usage
os.environ["USE_TORCH"] = "1"  # force PyTorch

def _emb_model():
    # Free, good quality & fast
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(text_and_metas, index_path: str):
    """
    text_and_metas: list of (text, metadata) tuples
    """
    if not text_and_metas:
        raise ValueError("No text to index.")
    texts = [t for t, _ in text_and_metas]
    metas = [m for _, m in text_and_metas]
    vs = FAISS.from_texts(texts, embedding=_emb_model(), metadatas=metas)
    vs.save_local(index_path)
    return vs

def load_vector_store(index_path: str):
    # `allow_dangerous_deserialization=True` is needed for newer langchain+faiss combos
    return FAISS.load_local(index_path, _emb_model(), allow_dangerous_deserialization=True)
