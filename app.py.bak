# app.py
import streamlit as st
import pandas as pd
from modules import portfolio_utils, visualizer, ai_explainer
import os
from dotenv import load_dotenv
load_dotenv()
from modules import stock_news
import yfinance as yf
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import glob, os
import plotly.express as px


st.set_page_config(page_title="StockPulse", layout="wide", initial_sidebar_state="expanded")
# Define possible variations of column names from different portfolio CSVs

# --- Dynamic column mapping (put near imports) ---


# --- Sidebar / Navigation ---
st.sidebar.title("StockPulse")
page = st.sidebar.radio("Navigate", ["Home",  "Dashboard", "Analytics", "Documents", "AI Explainer"])

# --- Home ---
if page == "Home":
    st.title("📈 StockPulse — Personal Portfolio Visualizer")
    

    # st.markdown("### Quick steps:")
    # st.markdown("""
    # 1. Upload your portfolio CSV in **Upload**.  
    # 2. Open **Dashboard** to see interactive charts.  
    # 3. Use **AI Explainer** to ask questions about your portfolio.
    # """)

    # # --- 1. Interactive sample portfolios ---
    # demo_options = {
    #     "Select a sample portfolio": None,
    #     "Tech Giants": "data/tech_giants.csv",
    #     "Green Energy": "data/green_energy.csv",
    #     "Top 10 ETFs": "data/top_10_etfs.csv",
    #     "sample_portfolio":"data/sample_portfolio.csv"
    # }
    # selected_demo = st.selectbox("Try a sample portfolio:", list(demo_options.keys()))
    # if selected_demo and demo_options[selected_demo]:
    #     sample_path = demo_options[selected_demo]
    #     try:
    #         sample = pd.read_csv(sample_path, parse_dates=["Date"])
    #         st.session_state["portfolio_df"] = sample
    #         st.success(f"Loaded sample portfolio: **{selected_demo}**. Go to Dashboard to explore.")
    #     except Exception as e:
    #         st.error(f"Failed to load sample portfolio: {e}")


    st.markdown("### 📰 Latest Stock Market News")
    # Define symbols you want
    # Define symbols
    
    tickers = {
        "DJIA": "^DJI",
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "VIX": "^VIX",
        "U.S. 10 Yr": "^TNX",
        "Crude Oil": "CL=F",
        "Gold": "GC=F",
        "Bitcoin": "BTC-USD"
    }
    cols = st.columns(len(tickers))

    for i, (name, symbol) in enumerate(tickers.items()):
        data = yf.Ticker(symbol).history(period="5d")
        
        if data.empty:
            price = None
            pct_change = None
        else:
            price = data["Close"].dropna().iloc[-1]
            prev_close = data["Close"].dropna().iloc[-2] if len(data["Close"].dropna()) > 1 else price
            pct_change = ((price - prev_close) / prev_close) * 100 if prev_close != 0 else 0
        
        color = "green" if pct_change and pct_change > 0 else "red"
        arrow = "↑" if pct_change and pct_change > 0 else "↓"

        with cols[i]:
            if price is not None:
                st.markdown(
                    f"""
                    <div style="text-align:center; min-width:100px;">
                        <b>{name}</b><br>
                        <span style="color:{color}; font-size:16px;">{price:,.2f}</span><br>
                        <span style="color:{color}; font-size:14px;">{pct_change:.2f}% {arrow}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align:center; min-width:100px;'><b>{name}</b><br>N/A</div>",
                    unsafe_allow_html=True
                )

    # cols = st.columns(len(tickers))

    # for i, (name, symbol) in enumerate(tickers.items()):
    #     data = yf.Ticker(symbol).history(period="5d")

    #     if data.empty:
    #         price = None
    #         pct_change = None
    #     else:
    #         price = data["Close"].dropna().iloc[-1]
    #         prev_close = data["Close"].dropna().iloc[-2] if len(data["Close"].dropna()) > 1 else price
    #         pct_change = ((price - prev_close) / prev_close) * 100 if prev_close != 0 else 0

    #     color = "green" if pct_change and pct_change > 0 else "red"
    #     arrow = "↑" if pct_change and pct_change > 0 else "↓"

    #     with cols[i]:
    #         if price is not None:
    #             st.markdown(
    #                 f"**{name}** "
    #                 f":{color}[{price:.2f}] "
    #                 f":{color}[{pct_change:.2f}%] {arrow}",
    #                 unsafe_allow_html=True
    #             )
    #         else:
    #             st.markdown(f"**{name}** N/A")


    news_type = st.radio("Choose news type:", ["General Market News", "Company News"], horizontal=True)
    symbol = None
    if news_type == "Company News":
        symbol = st.text_input("Enter stock symbol (e.g., AAPL)")

    if news_type == "General Market News":
        news_items = stock_news.fetch_general_news()
        stock_news.display_news(news_items)  # No symbol for general
    else:
        if symbol:
            news_items = stock_news.fetch_company_news(symbol.upper())
            stock_news.display_news(news_items)

  # Pass symbol here
        else:
            st.info("Please enter a stock symbol to see company news.")



    # --- 2. Showcase key features ---
    # st.markdown("### Why use StockPulse?")
    # features = {
    #     "📊 Interactive Dashboards": "Visualize your portfolio with rich charts and summaries.",
    #     "🤖 AI-powered Insights": "Ask natural language questions about your investments.",
    #     "🗂 Easy Upload & Management": "Quickly upload CSVs and manage multiple portfolios.",
    #     "📈 Performance Tracking": "Monitor gains, losses, and trends over time."
    # }
    # for feature, desc in features.items():
    #     st.markdown(f"**{feature}** — {desc}")

    # # st.markdown("---")

    # # # --- 3. Video / GIF demo (replace with your actual URL or local path) ---
    # # # st.markdown("### See it in action:")
    # # # st.video("https://streamable.com/e/your-demo-video")  # Replace with actual demo video URL

    # # st.markdown("---")
    # # --- GIF Carousel ---
    
    
    # # --- Live Data Preview ---
   
    # # --- Quick Stats ---
    



    # # --- 4. User testimonials ---
    # st.markdown("### What users say:")
    # testimonials = [
    #     "“StockPulse transformed how I view my investments — so easy and insightful!” — Alex G.",
    #     "“The AI explainer answered questions I didn’t even know how to ask.” — Priya K.",
    #     "“Beautiful dashboards and simple uploads. Highly recommend.” — Daniel M."
    # ]
    # for t in testimonials:
    #     st.markdown(f"> {t}")
elif page == "Dashboard":
    st.title("📊 Portfolio Dashboard")

    import glob, os

    # CSV Type Mapping (same as Analytics page)
    CSV_TYPES = {
        "Stocks Portfolio CSV": [
            "Symbol", "Investment", "Current Value", "Price",
            "Quantity", "Average Price", "Day Change %",
            "Day Change ₹", "Overall Change %", "Overall Change ₹"
        ],
        "Mutual Funds Portfolio CSV": [
            "Scheme Name", "Investment", "Current Value",
            "Units", "NAV", "Day Change %", "Day Change ₹",
            "Overall Change %", "Overall Change ₹"
        ],
        "Transaction History CSV": [
            "Date", "Symbol/Scheme", "Type", "Quantity/Units",
            "Price/NAV", "Amount"
        ],
        "P&L / Tax CSV": [
            "Symbol/Scheme", "Buy Date", "Sell Date", "Buy Price",
            "Sell Price", "Quantity/Units", "Buy Amount", "Sell Amount",
            "Profit/Loss", "Tax Paid"
        ]
    }

    # Select CSV type
    csv_type = st.selectbox("📂 Select your CSV type", list(CSV_TYPES.keys()))

    # List available CSV files in assets/
    csv_files = glob.glob("assets/*.csv")
    csv_names = [os.path.basename(f) for f in csv_files]

    # Session storage for uploaded file
    if "uploaded_portfolio" not in st.session_state:
        st.session_state["uploaded_portfolio"] = None

    uploaded_file = st.file_uploader("Upload your portfolio CSV file", type=["csv"])

    # Save to session state if uploaded
    if uploaded_file is not None:
        # Read file into DataFrame immediately, so the file object isn't lost
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["uploaded_portfolio"] = df
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()

    if st.session_state["uploaded_portfolio"] is None:
        st.info("Please select a CSV type and upload a CSV file to analyze.")
    else:
        try:
            df = st.session_state["uploaded_portfolio"]

            # ✅ Ensure required columns exist
            required_cols = CSV_TYPES[csv_type]
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                st.error(f"Uploaded file is missing required columns for {csv_type}: {', '.join(missing)}")
                st.stop()

            # Convert Date columns if available
            date_cols = [col for col in df.columns if "Date" in col]
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        except Exception as e:
            st.error(f"Error loading file: {e}")
            df = None


        if df is not None:
            st.sidebar.subheader("Filters")

            # Date range filter (works if any Date column present)
            if "Date" in df.columns and df["Date"].notnull().any():
                min_date = df["Date"].min().date()
                max_date = df["Date"].max().date()
                start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
                end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=max_date, value=max_date)
                df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

            # Name filter (Symbol / Scheme)
            name_col = None
            if "Symbol" in df.columns:
                name_col = "Symbol"
            elif "Scheme Name" in df.columns:
                name_col = "Scheme Name"
            elif "Symbol/Scheme" in df.columns:
                name_col = "Symbol/Scheme"

            if name_col:
                names = df[name_col].dropna().unique().tolist()
                selected_names = st.sidebar.multiselect(f"Select {name_col}", options=names, default=names)
                df = df[df[name_col].isin(selected_names)]

            # --- DASHBOARD KPIs + CHARTS ---
            st.subheader("📊 Key Portfolio Stats")

            if csv_type in ["Stocks Portfolio CSV", "Mutual Funds Portfolio CSV"]:
                total_invested = df["Investment"].sum()
                current_value = df["Current Value"].sum()
                total_gain = current_value - total_invested
                gain_pct = (total_gain / total_invested * 100) if total_invested != 0 else 0

                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("Total Invested", f"₹{total_invested:,.2f}")
                kpi2.metric("Current Value", f"₹{current_value:,.2f}", delta=f"{gain_pct:.2f}%")
                kpi3.metric("Total Gain/Loss", f"₹{total_gain:,.2f}", delta_color="normal")

                # Pie chart by investment
                st.subheader("Holdings by Investment")
                fig_pie = px.pie(df, names=name_col, values="Investment", title="Portfolio Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)

                # Price history
                if "Date" in df.columns and df["Date"].notnull().any():
                    st.subheader("Price History Over Time")
                    fig_line = px.line(df, x="Date", y="Price" if "Price" in df.columns else "NAV",
                                       color=name_col, markers=True)
                    st.plotly_chart(fig_line, use_container_width=True)

                # Gain/Loss Trend
                df["Gain/Loss"] = df["Current Value"] - df["Investment"]
                if "Date" in df.columns and df["Date"].notnull().any():
                    st.subheader("Gain/Loss Trend Over Time")
                    fig_gain = px.line(df, x="Date", y="Gain/Loss", color=name_col, markers=True)
                    st.plotly_chart(fig_gain, use_container_width=True)

            elif csv_type == "Transaction History CSV":
                if "Date" in df.columns:
                    st.subheader("Transactions Over Time")
                    fig_line = px.line(df, x="Date", y="Amount", color="Symbol/Scheme", markers=True)
                    st.plotly_chart(fig_line, use_container_width=True)

            elif csv_type == "P&L / Tax CSV":
                st.subheader("Profit/Loss by Asset")
                fig_bar = px.bar(df, x="Symbol/Scheme", y="Profit/Loss",
                                 color="Profit/Loss", text="Profit/Loss")
                st.plotly_chart(fig_bar, use_container_width=True)



elif page == "Analytics":
    st.title("📈 Portfolio Analytics")

    # CSV Type Mapping
    CSV_TYPES = {
        "Stocks Portfolio CSV": [
            "Symbol", "Investment", "Current Value", "Price",
            "Quantity", "Average Price", "Day Change %",
            "Day Change ₹", "Overall Change %", "Overall Change ₹"
        ],
        "Mutual Funds Portfolio CSV": [
            "Scheme Name", "Investment", "Current Value",
            "Units", "NAV", "Day Change %", "Day Change ₹",
            "Overall Change %", "Overall Change ₹"
        ],
        "Transaction History CSV": [
            "Date", "Symbol/Scheme", "Type", "Quantity/Units",
            "Price/NAV", "Amount"
        ],
        "P&L / Tax CSV": [
            "Symbol/Scheme", "Buy Date", "Sell Date", "Buy Price",
            "Sell Price", "Quantity/Units", "Buy Amount", "Sell Amount",
            "Profit/Loss", "Tax Paid"
        ]
    }

    # Ask user which CSV type they are uploading
    csv_type = st.selectbox(
    "Select CSV type",
    [
        "Stocks Portfolio CSV",
        "Mutual Funds Portfolio CSV",
        "Transaction History CSV",
        "P&L / Tax CSV"
    ]
)


    # Session storage for uploaded file
    if "uploaded_portfolio" not in st.session_state:
        st.session_state["uploaded_portfolio"] = None

    uploaded_file = st.file_uploader("Upload your portfolio CSV file", type=["csv"])

    # Save to session state if uploaded
    if uploaded_file is not None:
        st.session_state["uploaded_portfolio"] = uploaded_file

    if st.session_state["uploaded_portfolio"] is None:
        st.info("Please select a CSV type and upload a CSV file to analyze.")
    else:
        try:
            df = pd.read_csv(st.session_state["uploaded_portfolio"])

            # ✅ Ensure required columns exist
            required_cols = CSV_TYPES[csv_type]
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                st.error(f"Uploaded file is missing required columns for {csv_type}: {', '.join(missing)}")
                st.stop()

            # Convert Date columns if available
            date_cols = [col for col in df.columns if "Date" in col]
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        except Exception as e:
            st.error(f"Error loading file: {e}")
            df = None

        if df is not None:
            st.sidebar.subheader("Filters")

            # Date filter if applicable
            if "Date" in df.columns and df["Date"].notnull().any():
                min_date = df["Date"].min().date()
                max_date = df["Date"].max().date()
                start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
                end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=max_date, value=max_date)
                df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

            # Symbol/Scheme filter
            name_col = None
            if "Symbol" in df.columns:
                name_col = "Symbol"
            elif "Scheme Name" in df.columns:
                name_col = "Scheme Name"
            elif "Symbol/Scheme" in df.columns:
                name_col = "Symbol/Scheme"

            if name_col:
                names = df[name_col].dropna().unique().tolist()
                selected_names = st.sidebar.multiselect(f"Select {name_col}", options=names, default=names)
                df = df[df[name_col].isin(selected_names)]

            # --- ANALYTICS FOR EACH CSV TYPE ---
            st.subheader("📊 Analysis")

            if csv_type == "Stocks Portfolio CSV":
                summary = df.groupby("Symbol").agg(
                    Total_Investment=("Investment", "sum"),
                    Current_Value=("Current Value", "sum"),
                    Avg_Price=("Price", "mean")
                ).reset_index()
                summary["Gain/Loss"] = summary["Current_Value"] - summary["Total_Investment"]
                summary["Gain/Loss %"] = (summary["Gain/Loss"] / summary["Total_Investment"] * 100).round(2)
                st.dataframe(summary)

                fig_pie = px.pie(summary, names="Symbol", values="Current_Value", title="Portfolio Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)

                fig_bar = px.bar(summary, x="Symbol", y="Gain/Loss %", color="Gain/Loss %", text="Gain/Loss %")
                st.plotly_chart(fig_bar, use_container_width=True)

                                # Investment vs Current Value bar chart
                fig_invest_vs_value = px.bar(summary, x="Symbol",
                                            y=["Total_Investment", "Current_Value"],
                                            barmode="group",
                                            title="Investment vs Current Value")
                st.plotly_chart(fig_invest_vs_value, use_container_width=True)

                # Scatter plot: Risk vs Return
                fig_scatter = px.scatter(summary, x="Total_Investment",
                                        y="Gain/Loss %",
                                        size="Current_Value",
                                        color="Gain/Loss %",
                                        title="Risk vs Return")
                st.plotly_chart(fig_scatter, use_container_width=True)

                # (Optional) Line chart if you have a historical price column
                if "Price" in df.columns and "Date" in df.columns:
                    fig_price_trend = px.line(df, x="Date", y="Price", color="Symbol",
                                            title="Stock Price Trend Over Time")
                    st.plotly_chart(fig_price_trend, use_container_width=True)


            elif csv_type == "Mutual Funds Portfolio CSV":
                summary = df.groupby("Scheme Name").agg(
                    Total_Investment=("Investment", "sum"),
                    Current_Value=("Current Value", "sum"),
                    Avg_NAV=("NAV", "mean")
                ).reset_index()
                summary["Gain/Loss"] = summary["Current_Value"] - summary["Total_Investment"]
                summary["Gain/Loss %"] = (summary["Gain/Loss"] / summary["Total_Investment"] * 100).round(2)
                st.dataframe(summary)

                fig_pie = px.pie(summary, names="Scheme Name", values="Current_Value", title="Portfolio Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)

                fig_bar = px.bar(summary, x="Scheme Name", y="Gain/Loss %", color="Gain/Loss %", text="Gain/Loss %")
                st.plotly_chart(fig_bar, use_container_width=True)

                                # NAV Trend Over Time
                if "NAV" in df.columns and "Date" in df.columns:
                    fig_nav_trend = px.line(df, x="Date", y="NAV", color="Scheme Name",
                                            title="NAV Trend Over Time")
                    st.plotly_chart(fig_nav_trend, use_container_width=True)

                # SIP vs Lump sum (if transaction type column available)
                if "Type" in df.columns:
                    sip_lumpsum = df.groupby("Type")["Investment"].sum().reset_index()
                    fig_sip = px.bar(sip_lumpsum, x="Type", y="Investment",
                                    title="SIP vs Lump Sum Investments")
                    st.plotly_chart(fig_sip, use_container_width=True)

                # Donut Chart (Asset Allocation if asset type column exists)
                if "Asset Type" in df.columns:
                    fig_asset = px.pie(df, names="Asset Type", values="Current Value",
                                    hole=0.4, title="Asset Allocation")
                    st.plotly_chart(fig_asset, use_container_width=True)


                

            elif csv_type == "Transaction History CSV":
                if "Date" in df.columns:
                    fig_line = px.line(df, x="Date", y="Amount", color="Symbol/Scheme", title="Transactions Over Time")
                    st.plotly_chart(fig_line, use_container_width=True)
                    # Buy vs Sell per month (Stacked Bar Chart)
                    df['Month'] = df['Date'].dt.to_period('M')
                    buy_sell = df.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
                    fig_buy_sell = px.bar(buy_sell, x="Month", y="Amount", color="Type",
                                        title="Buy vs Sell per Month")
                    st.plotly_chart(fig_buy_sell, use_container_width=True)

                    # Allocation by Sector (if sector column exists)
                    if "Sector" in df.columns:
                        fig_sector = px.pie(df, names="Sector", values="Amount",
                                            title="Allocation by Sector")
                        st.plotly_chart(fig_sector, use_container_width=True)


            elif csv_type == "P&L / Tax CSV":
                fig_bar = px.bar(df, x="Symbol/Scheme", y="Profit/Loss", color="Profit/Loss", text="Profit/Loss")
                st.plotly_chart(fig_bar, use_container_width=True)
                # Cumulative Profit/Loss Trend
                if "Date" in df.columns:
                    df_sorted = df.sort_values("Date")
                    df_sorted["Cumulative P/L"] = df_sorted["Profit/Loss"].cumsum()
                    fig_cumulative = px.line(df_sorted, x="Date", y="Cumulative P/L",
                                            title="Cumulative Profit/Loss Trend")
                    st.plotly_chart(fig_cumulative, use_container_width=True)

                # Monthly Gain/Loss (Waterfall style using bar chart)
                if "Date" in df.columns:
                    df['Month'] = df['Date'].dt.to_period('M')
                    monthly_pl = df.groupby('Month')["Profit/Loss"].sum().reset_index()
                    fig_monthly = px.bar(monthly_pl, x="Month", y="Profit/Loss",
                                        title="Monthly Profit/Loss")
                    st.plotly_chart(fig_monthly, use_container_width=True)



# --- Documents ---
elif page == "Documents":
    st.title("🗂 Documents")
    st.info("Upload PDFs or notes related to your portfolio.")
    uploaded_doc = st.file_uploader("Upload PDF (or image) for documentation", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_doc:
        with open(os.path.join("assets", uploaded_doc.name), "wb") as f:
            f.write(uploaded_doc.getbuffer())
        st.success(f"Saved to assets/{uploaded_doc.name}")

    # st.markdown("**Existing assets**")
    # import glob
    # files = glob.glob("assets/*")
    # for f in files:
    #     st.write(f)

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
