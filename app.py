import os
import streamlit as st
import subprocess
import sys
from utils.groq_llm import GroqLLM
from utils.vectorstore_faiss import load_faiss_vectorstore
from langchain.schema import Document
from utils.information_retrievers import get_wikipedia_summary, get_stock_data

st.set_page_config(page_title="Company Intelligence Assistant", page_icon="💼", layout="wide")
st.title("📈 Company Intelligence Assistant")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Company Selection")
    company_name = st.text_input("Company Name", value="Tesla")
    ticker = st.text_input("Stock Ticker (e.g., TSLA, MSFT)", value="TSLA")
    
    st.header("RAG Settings")
    top_k = st.slider("Top-k chunks", 3, 12, 5)
    model = st.selectbox("Groq model", ["llama3-70b-8192", "mixtral-8x7b-32768"])
    
    st.header("Update Data")
    if st.button("Update News Index"):
        st.info("Starting background update...")
        command = [sys.executable, "run_update.py", "--company", company_name]
        subprocess.Popen(command)

# --- Main Page Layout ---
col1, col2 = st.columns([0.6, 0.4])

# --- Helper function to build the prompt (you can also move this to a utils file) ---
def build_prompt(query: str, docs: list[Document]) -> str:
    sources = []
    seen = set()
    for d in docs:
        u = d.metadata.get("source", "")
        if u and u not in seen:
            sources.append(u)
            seen.add(u)

    numbered = {u: i + 1 for i, u in enumerate(sources)}
    ctx_blocks = []
    for d in docs:
        src = d.metadata.get("source", "")
        cite = f"[{numbered.get(src)}]" if src in numbered else ""
        ctx_blocks.append(f"{d.page_content} {cite}")

    sources_list = "\n".join([f"[{i+1}] {u}" for i, u in enumerate(sources)]) or "None"

    return f"""
Answer the user's question using ONLY the following context. Cite sources inline like [1], [2].

Question:
{query}

Context:
{"\n\n---\n\n".join(ctx_blocks)}

Sources:
{sources_list}
"""

with col1:
    st.header(f"Intelligence Briefing for {company_name}")
    
    with st.container(border=True):
        st.subheader("📝 Wikipedia Summary")
        with st.spinner("Fetching Wikipedia..."):
            summary = get_wikipedia_summary(company_name)
        st.write(summary)

    with st.container(border=True):
        st.subheader("🤖 Ask a Question (Based on News Index)")
        index_path = f"faiss_index_{company_name.lower()}"
        vs = None
        try:
            vs = load_faiss_vectorstore(index_path)
        except Exception:
            st.warning(f"News index for '{company_name}' not found. Click 'Update News Index' in the sidebar.")
        
        question = st.text_input("Your question", "What are the latest developments and strategy?")
        
        # --- This is the fully implemented RAG logic ---
        if st.button("Get Answer"):
            if not vs:
                st.error("The News Index is not loaded. Please run an update first.")
            elif not question:
                st.warning("Please enter a question.")
            else:
                with st.spinner("Searching for context..."):
                    docs = vs.similarity_search(
                        question,
                        k=top_k,
                        filter={"company": company_name.lower()}
                    )
                
                if not docs:
                    st.error("Could not find any relevant documents in the news index to answer this question.")
                else:
                    prompt = build_prompt(question, docs)
                    with st.spinner(f"Asking Groq ({model})..."):
                        try:
                            llm = GroqLLM(model=model)
                            answer = llm.predict(prompt)
                            st.markdown(answer)
                        except Exception as e:
                            st.error(f"❌ Groq call failed: {e}")

with col2:
    st.header(f"Financial Snapshot ({ticker.upper()})")
    
    with st.container(border=True):
        st.subheader("📈 Stock Performance")
        if ticker:
            with st.spinner("Fetching stock data..."):
                stock_data = get_stock_data(ticker)
            if "error" in stock_data:
                st.error(stock_data["error"])
            else:
                current_price = stock_data.get("current_price", 0)
                prev_close = stock_data.get("previous_close", 0)
                delta = current_price - prev_close if current_price and prev_close else 0
                st.metric(
                    label=f"Current Price",
                    value=f"${current_price:,.2f}" if current_price else "N/A",
                    delta=f"{delta:,.2f}" if delta else None
                )
                st.line_chart(stock_data['history']['Close'], use_container_width=True)
                st.write(f"**Open:** ${stock_data.get('open', 0):,.2f}")
                st.write(f"**Day High:** ${stock_data.get('day_high', 0):,.2f}")
                st.write(f"**Day Low:** ${stock_data.get('day_low', 0):,.2f}")
                st.write(f"**Market Cap:** ${stock_data.get('market_cap', 0):,}")
        else:
            st.info("Enter a stock ticker to see financial data.")