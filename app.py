import streamlit as st
import pandas as pd
from modules import portfolio_utils, visualizer, ai_explainer

st.set_page_config(page_title="📈 StockPulse", layout="wide")

st.title("📈 StockPulse: Personal Portfolio Visualizer + AI Market Explainer")

# Upload CSV
uploaded_file = st.file_uploader("Upload your stock portfolio CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["portfolio_df"] = df
    st.success("✅ File uploaded and data loaded!")

    # Portfolio Summary
    st.subheader("📊 Portfolio Summary")
    summary = portfolio_utils.generate_summary(df)
    st.dataframe(summary)

    # Visualizations
    st.subheader("📈 Visualizations")
    visualizer.display_charts(df)

    # AI Explainer
    st.subheader("🤖 AI Market Explainer")
    question = st.text_input("Ask a question about your portfolio or market trends:")
    if question:
        answer = ai_explainer.get_explanation(question, df)
        st.success(answer)
else:
    st.info("📁 Please upload your portfolio CSV file to begin.")
