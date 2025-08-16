from utils.scraping import fetch_news, scrape_full_text
from utils.processing import clean_text, chunk_with_meta
from utils.vectorstore_faiss import create_faiss_vectorstore
from config import NEWS_API_KEY

def update_company_data(company_name: str, max_articles: int = 8):
    # Pass the API key here!
    articles = fetch_news(company_name, api_key=NEWS_API_KEY, max_articles=max_articles)

    text_and_metas = []
    for a in articles:
        full_text = clean_text(scrape_full_text(a["url"]))
        if not full_text or len(full_text) < 300:
            continue
        meta = {
            "source": a["url"],
            "title": a["title"],
            "publishedAt": a.get("publishedAt", ""),
            "sourceName": a.get("sourceName", ""),
            "company": company_name.lower()
        }
        chunks = chunk_with_meta(full_text, meta, chunk_size=1100, overlap=200)
        text_and_metas.extend(chunks)

    if not text_and_metas:
        raise RuntimeError("No usable articles scraped.")


    # Define a local path for the index file
    index_path = f"faiss_index_{company_name.lower()}"
    
    # Save to FAISS instead of Pinecone
    create_faiss_vectorstore(text_and_metas, index_path=index_path)
    
    print(f"Indexed {len(text_and_metas)} chunks into FAISS.")
    return len(text_and_metas)