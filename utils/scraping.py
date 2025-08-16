import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def fetch_news(company_name: str, api_key: str, max_articles: int = 8) -> List[Dict]:
    """
    Fetch latest news articles from NewsAPI for a given company.

    Args:
        company_name (str): The company to search for.
        api_key (str): NewsAPI API key.
        max_articles (int): Maximum number of articles to fetch.

    Returns:
        List[Dict]: A list of article metadata dictionaries.
    """
    url = (
        f"https://newsapi.org/v2/everything?q={company_name}"
        f"&language=en&sortBy=publishedAt&pageSize={max_articles}&apiKey={api_key}"
    )
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        articles = []
        for a in data.get("articles", [])[:max_articles]:
            articles.append({
                "title": a.get("title", ""),
                "url": a.get("url", ""),
                "publishedAt": a.get("publishedAt", ""),
                "sourceName": (a.get("source") or {}).get("name", "")
            })
        if not articles:
            print(f"[INFO] No articles found for {company_name}")
        return articles
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] fetch_news network request failed: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] fetch_news failed: {e}")
        return []


def scrape_full_text(url: str) -> str:
    """
    Scrape full text from a news article URL using BeautifulSoup.

    Args:
        url (str): URL of the news article.

    Returns:
        str: Cleaned article text.
    """
    if not url:
        return ""
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Prefer <article> paragraphs first, fallback to all <p> tags
        candidates = soup.select("article p") or soup.find_all("p")
        paragraphs = [p.get_text(" ", strip=True) for p in candidates if p.get_text(strip=True)]
        # Keep only paragraphs longer than 40 characters
        text = "\n".join([t for t in paragraphs if len(t) > 40])
        if not text:
            print(f"[INFO] No substantial text found at URL: {url}")
        return text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] scrape_full_text network request failed: {e}")
        return ""
    except Exception as e:
        print(f"[ERROR] scrape_full_text failed: {e}")
        return ""
