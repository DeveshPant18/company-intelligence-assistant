import yfinance as yf
import wikipediaapi # <-- Correct import statement

def get_wikipedia_summary(company_name: str) -> str:
    """
    Fetches a summary of a company from Wikipedia.
    """
    try:
        # Use a proper user-agent for the API call
        wiki = wikipediaapi.Wikipedia(
            user_agent='CompanyIntelligenceBot/1.0 (contact@example.com)',
            language='en'
        )
        page = wiki.page(company_name) # No auto_suggest in this library, it handles redirects
        
        if page.exists():
            # Return first 700 characters of the summary
            return page.summary[0:700] + "..."
        else:
            return f"Could not find a Wikipedia page for '{company_name}'."
            
    except Exception as e:
        return f"An error occurred while fetching from Wikipedia: {e}"

def get_stock_data(ticker: str) -> dict:
    """
    Fetches stock data for a given ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")
        
        if hist.empty:
            return {"error": f"No data found for ticker '{ticker}'. It may be delisted or incorrect."}

        info = stock.info
        price_data = {
            "current_price": info.get('currentPrice', info.get('regularMarketPrice')),
            "previous_close": info.get('previousClose'),
            "open": info.get('open'),
            "day_high": info.get('dayHigh'),
            "day_low": info.get('dayLow'),
            "volume": info.get('volume'),
            "market_cap": info.get('marketCap'),
            "history": hist
        }
        return price_data
    except Exception as e:
        return {"error": f"An error occurred while fetching stock data: {e}"}