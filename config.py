import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")   # <-- new
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")  # default region

# Fail fast if missing keys
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing in .env file")
if not NEWS_API_KEY:
    raise ValueError("❌ NEWS_API_KEY is missing in .env file")
if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY is missing in .env file")
