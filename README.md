# 📈 Company Intelligence Assistant

A multi-faceted dashboard built with Streamlit that provides a 360-degree view of public companies. This tool combines real-time financial data, encyclopedic summaries, and a news-based Q&A system powered by a Retrieval-Augmented Generation (RAG) pipeline.


---

## ✨ Features

* **Financial Snapshot:** Displays real-time stock prices, historical performance charts, and key metrics like market cap and volume using the `yfinance` library.
* **Company Overview:** Fetches and displays concise company summaries directly from Wikipedia.
* **News-Based Q&A (RAG):** Ask questions in natural language and get answers synthesized from recent news articles. This is powered by a local FAISS vector store, Sentence Transformers for embeddings, and the Groq API for fast LLM inference.
* **On-Demand Data Updates:** A user-friendly interface to ingest and index news for any company, which runs as a non-blocking background process.
* **Flexible LLM Choice:** Easily switch between different high-speed models available on Groq (e.g., Llama3, Mixtral).

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Inference:** [Groq](https://groq.com/)
* **Core AI/RAG Framework:** [LangChain](https://www.langchain.com/)
* **Vector Store:** [FAISS](https://github.com/facebookresearch/faiss) (local, CPU-based)
* **Embeddings:** [Sentence Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`)
* **Data Sources:**
    * [Yahoo! Finance (`yfinance`)](https://pypi.org/project/yfinance/) for stock data.
    * [Wikipedia (`wikipedia-api`)](https://pypi.org/project/wikipedia-api/) for company summaries.
    * [NewsAPI](https://newsapi.org/) for news articles.
* **Language:** Python 3.10+

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

* Python 3.10 or higher
* Git

### 2. Clone the Repository

```bash
git clone <https://github.com/DeveshPant18/company-intelligence-assistant.git>
```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

Create a `requirements.txt` file with the content below, and then install the packages.

**`requirements.txt`:**
```
streamlit
langchain
langchain-community
groq
python-dotenv
requests
beautifulsoup4
faiss-cpu
sentence-transformers
yfinance
wikipedia-api
```

**Installation command:**
```bash
pip install -r requirements.txt
```

### 5. Set Up API Keys

You need to provide API keys for Groq and NewsAPI.

1.  Make a copy of the `.env.example` file (or create a new file) and name it `.env`.
2.  Add your keys to the `.env` file:

**`.env` file:**
```
GROQ_API_KEY="gsk_YourGroqApiKey"
NEWS_API_KEY="YourNewsApiKey"
```

---

## 🏃‍♀️ How to Use the Application

### Step 1: Ingest News Data

Before you can ask questions, you must first build a news index for a company. Run the update script from your terminal.

* **Example for Tesla:**
    ```bash
    python run_update.py --company "Tesla"
    ```
* **Example for Microsoft:**
    ```bash
    python run_update.py --company "Microsoft"
    ```
This will create a FAISS index in the `vector_store/` directory (e.g., `vector_store/faiss_index_tesla`).

### Step 2: Launch the Streamlit App

Once the index is built, you can start the web application.

```bash
streamlit run app.py
```

Your browser should automatically open to the application. You can now select a company, view its financial data, and ask questions based on the news index you created. You can also trigger new updates directly from the sidebar in the app.

---

## 📁 Project Structure

```
.
├── utils/
│   ├── data_pipeline.py        # Combines scraping and processing
│   ├── groq_llm.py             # Custom LangChain wrapper for Groq
│   ├── information_retrievers.py # Functions for yfinance and Wikipedia
│   ├── processing.py           # Text cleaning and chunking
│   ├── scraping.py             # NewsAPI and article scraping
│   └── vectorstore_faiss.py    # Manages FAISS index creation/loading
├── vector_store/
│   └── .gitkeep                # Directory for saved FAISS indexes
├── app.py                      # The main Streamlit application
├── config.py                   # Loads environment variables
├── run_update.py               # Command-line script to ingest data
├── requirements.txt            # Project dependencies
└── .env                        # API keys (not committed to Git)
```

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.