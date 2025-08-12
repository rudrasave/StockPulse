import requests
from datetime import datetime, timedelta
import streamlit as st
import os

API_KEY = os.getenv("FINNHUB_API_KEY")  # Load API key from environment

if not API_KEY:
    st.error("Finnhub API key not found! Please set FINNHUB_API_KEY in your environment.")
def fetch_quote(symbol):
    """Fetch current price and percentage change for a given symbol."""
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    return {
        "price": data.get("c"),  # Current price
        "change_percent": data.get("dp")  # % change
    }

# ---------------- Fetch News ----------------
def fetch_general_news():
    url = f"https://finnhub.io/api/v1/news?category=general&token={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        st.error("Failed to fetch general news.")
        return []
    return res.json()

def fetch_company_news(symbol):
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={week_ago.date()}&to={today.date()}&token={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        st.error(f"Failed to fetch news for {symbol}.")
        return []
    return res.json()

# ---------------- Fetch Stock Quotes ----------------
def fetch_stock_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    return {
        "price": data.get("c"),
        "percent_change": data.get("dp")
    }

# ---------------- Display Styled News ----------------
def display_news(news_items, limit=10, symbol=None):

    if not news_items:
        st.write("No news available.")
        return

    for item in news_items[:limit]:
        col1, col2 = st.columns([1, 4])

        with col1:
            if item.get("image"):
                st.image(item["image"], use_container_width=True)

        with col2:
            st.markdown(f"### [{item['headline']}]({item['url']})")
            summary = item.get("summary", "")
            if summary:
                st.write(summary)
            dt = datetime.fromtimestamp(item.get("datetime", 0))
            st.write(f"*Source:* {item.get('source', 'Unknown')} | *Date:* {dt.strftime('%Y-%m-%d %H:%M')}")
        st.markdown("---")
