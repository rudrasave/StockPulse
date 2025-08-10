# app.py
import streamlit as st
import pandas as pd
from modules import portfolio_utils, visualizer, ai_explainer
import os
from dotenv import load_dotenv
load_dotenv()
from modules import stock_news
import yfinance as yf

st.set_page_config(page_title="StockPulse", layout="wide", initial_sidebar_state="expanded")

# --- Sidebar / Navigation ---
st.sidebar.title("StockPulse")
page = st.sidebar.radio("Navigate", ["Home",  "Dashboard", "Analytics", "Documents", "AI Explainer"])

# --- Home ---
if page == "Home":
    st.title("📈 StockPulse — Personal Portfolio Visualizer")
    

    st.markdown("### Quick steps:")
    st.markdown("""
    1. Upload your portfolio CSV in **Upload**.  
    2. Open **Dashboard** to see interactive charts.  
    3. Use **AI Explainer** to ask questions about your portfolio.
    """)

    # --- 1. Interactive sample portfolios ---
    demo_options = {
        "Select a sample portfolio": None,
        "Tech Giants": "data/tech_giants.csv",
        "Green Energy": "data/green_energy.csv",
        "Top 10 ETFs": "data/top_10_etfs.csv",
        "sample_portfolio":"data/sample_portfolio.csv"
    }
    selected_demo = st.selectbox("Try a sample portfolio:", list(demo_options.keys()))
    if selected_demo and demo_options[selected_demo]:
        sample_path = demo_options[selected_demo]
        try:
            sample = pd.read_csv(sample_path, parse_dates=["Date"])
            st.session_state["portfolio_df"] = sample
            st.success(f"Loaded sample portfolio: **{selected_demo}**. Go to Dashboard to explore.")
        except Exception as e:
            st.error(f"Failed to load sample portfolio: {e}")


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
    st.markdown("### Why use StockPulse?")
    features = {
        "📊 Interactive Dashboards": "Visualize your portfolio with rich charts and summaries.",
        "🤖 AI-powered Insights": "Ask natural language questions about your investments.",
        "🗂 Easy Upload & Management": "Quickly upload CSVs and manage multiple portfolios.",
        "📈 Performance Tracking": "Monitor gains, losses, and trends over time."
    }
    for feature, desc in features.items():
        st.markdown(f"**{feature}** — {desc}")

    # st.markdown("---")

    # # --- 3. Video / GIF demo (replace with your actual URL or local path) ---
    # # st.markdown("### See it in action:")
    # # st.video("https://streamable.com/e/your-demo-video")  # Replace with actual demo video URL

    # st.markdown("---")
    # --- GIF Carousel ---
    
    
    # --- Live Data Preview ---
   
    # --- Quick Stats ---
    



    # --- 4. User testimonials ---
    st.markdown("### What users say:")
    testimonials = [
        "“StockPulse transformed how I view my investments — so easy and insightful!” — Alex G.",
        "“The AI explainer answered questions I didn’t even know how to ask.” — Priya K.",
        "“Beautiful dashboards and simple uploads. Highly recommend.” — Daniel M."
    ]
    for t in testimonials:
        st.markdown(f"> {t}")

elif page == "Dashboard":
    st.title("📊 Dashboard")

    # Step 1: List uploaded CSV files from assets folder
    import glob, os
    csv_files = glob.glob("assets/*.csv")
    csv_names = [os.path.basename(f) for f in csv_files]

    if not csv_files:
        st.info("No uploaded CSV files found in 'assets'. Please upload files first.")
    else:
        # Step 2: Dropdown to select file
        selected_file_name = st.selectbox("Select portfolio file", csv_names)
        selected_file_path = os.path.join("assets", selected_file_name)

        # Step 3: Load selected file
        try:
            df = pd.read_csv(selected_file_path)
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
            st.session_state["portfolio_df"] = df
        except Exception as e:
            st.error(f"Error loading {selected_file_name}: {e}")
            df = None

        # Step 4: Show dashboard if file loaded
        if df is not None:
            st.sidebar.subheader("Filters")

            # Date range filter
            min_date = df["Date"].min().date()
            max_date = df["Date"].max().date()
            start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
            default_end = max(start_date, max_date)
            end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=max_date, value=default_end)

            # Stock filter
            symbols = df["Symbol"].unique().tolist()
            selected_symbols = st.sidebar.multiselect("Select Stocks", options=symbols, default=symbols)

            # Filter dataframe
            filtered_df = df[
                (df["Date"] >= pd.to_datetime(start_date)) &
                (df["Date"] <= pd.to_datetime(end_date)) &
                (df["Symbol"].isin(selected_symbols) if selected_symbols else True)
            ]

            # KPIs
            st.subheader("Key Performance Indicators")
            summary_df = portfolio_utils.generate_summary_df(filtered_df)
            total_value = float(summary_df.loc[summary_df["Metric"] == "Current Value (approx.)", "Value"].str.replace(",", "").astype(float))
            total_gain_str = summary_df.loc[summary_df["Metric"] == "Total Gain/Loss (approx.)", "Value"].values[0]
            total_gain = float(total_gain_str.replace(",", ""))

            gain_color = "green" if total_gain >= 0 else "red"

            cols = st.columns(3)
            cols[0].metric("Total Portfolio Value", f"${total_value:,.2f}")
            cols[1].metric("Total Gain/Loss", f"${total_gain:,.2f}", delta=f"${total_gain:,.2f}", delta_color="normal")
            cols[2].metric("Number of Stocks", len(selected_symbols))

            # Visualizations
            st.subheader("Holdings Pie Chart")
            fig_pie = visualizer.plot_holdings_pie(filtered_df)
            if fig_pie:
                st.plotly_chart(fig_pie, use_container_width=True)

            st.subheader("Price History")
            fig_line = visualizer.plot_price_history(filtered_df)
            if fig_line:
                st.plotly_chart(fig_line, use_container_width=True)


# # --- Upload ---
# elif page == "Upload":
#     st.title("📤 Upload Portfolio")
#     st.info("CSV must contain Date, Symbol, Close columns. If single-stock CSV lacks Symbol, you'll be prompted to provide it.")
#     uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
#     if uploaded_file:
#         try:
#             df = pd.read_csv(uploaded_file)
#             # parse date if a Date column exists
#             if "Date" in df.columns:
#                 df["Date"] = pd.to_datetime(df["Date"])
#             # if no symbol, prompt user
#             if "Symbol" not in df.columns:
#                 ticker = st.text_input("CSV has no Symbol column. Enter the ticker for this file (e.g. AAPL):")
#                 if ticker:
#                     df["Symbol"] = ticker.upper()
#             st.session_state["portfolio_df"] = df
#             st.success("File uploaded and stored in session.")
#             st.write(df.head())
#         except Exception as e:
#             st.error(f"Failed to read CSV: {e}")
#     # st.markdown("---")
#     # st.warning("Please upload a CSV file to proceed.")

# # --- Dashboard ---
# elif page == "Dashboard":
#     st.title("📊 Dashboard")
#     df = st.session_state.get("portfolio_df")
#     if df is None:
#         st.info("No portfolio loaded. Go to Upload and upload a CSV or load demo.")
#     else:
#         st.sidebar.subheader("Filters")

#         # Date range filter: allow single date or date range
#         min_date = df["Date"].min().date()
#         max_date = df["Date"].max().date()

#         # Use a single date input for start date
#         start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)

#         # Use a single date input for end date with default as max_date or start_date if start_date > max_date
#         default_end = max(start_date, max_date)
#         end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=max_date, value=default_end)

#         # Stock filter: allow empty selection = select all
#         symbols = df["Symbol"].unique().tolist()
#         selected_symbols = st.sidebar.multiselect("Select Stocks", options=symbols, default=symbols)

#         # Filter dataframe safely
#         filtered_df = df[
#             (df["Date"] >= pd.to_datetime(start_date)) & 
#             (df["Date"] <= pd.to_datetime(end_date)) & 
#             (df["Symbol"].isin(selected_symbols) if selected_symbols else True)
#         ]


#         # KPIs
#         st.subheader("Key Performance Indicators")
#         summary_df = portfolio_utils.generate_summary_df(filtered_df)
#         total_value = float(summary_df.loc[summary_df["Metric"] == "Current Value (approx.)", "Value"].str.replace(",", "").astype(float))
#         total_gain_str = summary_df.loc[summary_df["Metric"] == "Total Gain/Loss (approx.)", "Value"].values[0]
#         total_gain = float(total_gain_str.replace(",", ""))
        
#         gain_color = "green" if total_gain >= 0 else "red"
        
#         cols = st.columns(3)
#         cols[0].metric("Total Portfolio Value", f"${total_value:,.2f}")
#         st.write(f"Debug: total_gain = {total_gain}")

#         cols[1].metric("Total Gain/Loss", f"${total_gain:,.2f}", delta=f"${total_gain:,.2f}", delta_color="normal")
#         cols[2].metric("Number of Stocks", len(selected_symbols))

#         # Visualizations
#         st.subheader("Holdings Pie Chart")
#         fig_pie = visualizer.plot_holdings_pie(filtered_df)
#         if fig_pie:
#             st.plotly_chart(fig_pie, use_container_width=True)

#         st.subheader("Price History")
#         fig_line = visualizer.plot_price_history(filtered_df)
#         if fig_line:
#             st.plotly_chart(fig_line, use_container_width=True)


elif page == "Analytics":
    st.title("📈 Revenue & Performance Analytics")

    # --- Upload CSV ---
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        try:
            # Save uploaded file into assets folder
            os.makedirs("assets", exist_ok=True)
            file_path = os.path.join("assets", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Load into dataframe
            df = pd.read_csv(file_path)
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
            if "Symbol" not in df.columns:
                ticker = st.text_input("CSV has no Symbol column. Enter ticker (e.g. AAPL):")
                if ticker:
                    df["Symbol"] = ticker.upper()

            st.session_state["portfolio_df"] = df
            st.success(f"File uploaded and saved to assets/{uploaded_file.name}")

        except Exception as e:
            st.error(f"Failed to process CSV: {e}")

    # --- Show analytics only if a file is loaded ---
    df = st.session_state.get("portfolio_df")
    if df is None:
        st.info("Upload a portfolio CSV above to see analytics.")
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
