from langchain.schema import Document
import re

def clean_text(text: str) -> str:
    """Basic text cleaning: remove extra spaces, newlines, and repeated chars."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def chunk_with_meta(text: str, metadata: dict, chunk_size: int = 1100, overlap: int = 200) -> list[Document]:
    """
    Split text into overlapping chunks and attach metadata.
    Returns a list of LangChain Documents.
    """
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunk_text = text[start:end]
        chunks.append(Document(page_content=chunk_text, metadata=metadata))
        start += chunk_size - overlap
    return chunks
