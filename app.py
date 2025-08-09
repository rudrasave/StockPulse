# app.py
import streamlit as st
import pandas as pd
from modules import portfolio_utils, visualizer, ai_explainer
import os

st.set_page_config(page_title="StockPulse", layout="wide", initial_sidebar_state="expanded")

# --- Sidebar / Navigation ---
st.sidebar.title("StockPulse")
page = st.sidebar.radio("Navigate", ["Home", "Upload", "Dashboard", "Analytics", "Documents", "AI Explainer"])

# --- Home ---
if page == "Home":
    st.title("📈 StockPulse — Personal Portfolio Visualizer")
    st.write("Welcome! Use the sidebar to upload your portfolio, view dashboard analytics, or ask the AI explainer questions.")
    st.markdown("**Quick steps**:\n\n1. Upload your portfolio CSV in Upload.\n2. Open Dashboard to see charts.\n3. Use AI Explainer to ask questions about your portfolio.")
    if st.button("Load sample data into session (demo)"):
        sample = pd.read_csv("data/sample_portfolio.csv", parse_dates=["Date"])
        st.session_state["portfolio_df"] = sample
        st.success("Sample data loaded. Go to Dashboard.")

# --- Upload ---
elif page == "Upload":
    st.title("📤 Upload Portfolio")
    st.info("CSV must contain Date, Symbol, Close columns. If single-stock CSV lacks Symbol, you'll be prompted to provide it.")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            # parse date if a Date column exists
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
            # if no symbol, prompt user
            if "Symbol" not in df.columns:
                ticker = st.text_input("CSV has no Symbol column. Enter the ticker for this file (e.g. AAPL):")
                if ticker:
                    df["Symbol"] = ticker.upper()
            st.session_state["portfolio_df"] = df
            st.success("File uploaded and stored in session.")
            st.write(df.head())
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
    st.markdown("---")
    # st.warning("Please upload a CSV file to proceed.")

# --- Dashboard ---
elif page == "Dashboard":
    st.title("📊 Dashboard")
    df = st.session_state.get("portfolio_df")
    if df is None:
        st.info("No portfolio loaded. Go to Upload and upload a CSV or load demo.")
    else:
        st.subheader("Portfolio Summary")
        summary_df = portfolio_utils.generate_summary_df(df)
        st.dataframe(summary_df, use_container_width=True)

        st.subheader("Holdings Pie Chart")
        fig_pie = visualizer.plot_holdings_pie(df)
        if fig_pie:
            st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("Price History")
        fig_line = visualizer.plot_price_history(df)
        if fig_line:
            st.plotly_chart(fig_line, use_container_width=True)

# --- Analytics ---
elif page == "Analytics":
    st.title("📈 Revenue & Performance Analytics")
    df = st.session_state.get("portfolio_df")
    if df is None:
        st.info("Load portfolio data in Upload first.")
    else:
        st.subheader("Performance Summary")
        perf = portfolio_utils.performance_metrics(df)
        st.table(perf)

        st.subheader("Monthly Returns")
        fig_month = visualizer.plot_monthly_returns(df)
        if fig_month:
            st.plotly_chart(fig_month, use_container_width=True)

        st.subheader("Cumulative Return")
        fig_cum = visualizer.plot_cumulative_returns(df)
        if fig_cum:
            st.plotly_chart(fig_cum, use_container_width=True)

# --- Documents ---
elif page == "Documents":
    st.title("🗂 Documents")
    st.info("Upload PDFs or notes related to your portfolio.")
    uploaded_doc = st.file_uploader("Upload PDF (or image) for documentation", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_doc:
        with open(os.path.join("assets", uploaded_doc.name), "wb") as f:
            f.write(uploaded_doc.getbuffer())
        st.success(f"Saved to assets/{uploaded_doc.name}")

    st.markdown("**Existing assets**")
    import glob
    files = glob.glob("assets/*")
    for f in files:
        st.write(f)

# --- AI Explainer ---
elif page == "AI Explainer":
    st.title("🤖 AI Market Explainer")
    df = st.session_state.get("portfolio_df")
    question = st.text_input("Ask a question about your portfolio (e.g., 'Which stock shows strongest growth last 6 months?')")
    if st.button("Ask AI"):
        if df is None:
            st.error("Load a portfolio first in Upload.")
        elif not question.strip():
            st.error("Type a question first.")
        else:
            with st.spinner("Analyzing..."):
                answer = ai_explainer.get_explanation(question, df)
            st.markdown("**Answer:**")
            st.write(answer)
