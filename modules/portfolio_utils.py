# modules/portfolio_utils.py
import pandas as pd
import numpy as np

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # standardize common names
    df = df.copy()
    cols = {c.lower(): c for c in df.columns}
    # unify close column names
    if "close" in cols:
        df.rename(columns={cols["close"]: "Close"}, inplace=True)
    if "symbol" in cols:
        df.rename(columns={cols["symbol"]: "Symbol"}, inplace=True)
    if "date" in cols:
        df.rename(columns={cols["date"]: "Date"}, inplace=True)
    # if Date column exists, ensure datetime and set index
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values("Date", inplace=True)
        df.set_index("Date", inplace=False)
    return df

def generate_summary_df(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    if df.empty:
        return pd.DataFrame({"Metric": [], "Value": []})
    if "Symbol" not in df.columns:
        return pd.DataFrame({"Metric": ["Error"], "Value": ["No Symbol column found"]})
    # assume 1 share if not provided
    shares_col = None
    for name in ["Shares", "Quantity", "Qty"]:
        if name in df.columns:
            shares_col = name
            break
    if shares_col is None:
        df["Shares"] = 1
        shares_col = "Shares"

    # use latest close per symbol (last available date)
    last = df.sort_values("Date").groupby("Symbol").tail(1)
    last = last.set_index("Symbol")
    last_close = last["Close"]

    investment = 0.0
    if "Price" in df.columns:
        # if the CSV included buy price per row
        df["Investment"] = df[shares_col] * df["Price"]
        investment = df["Investment"].sum()
    elif "Investment" in df.columns:
        investment = df["Investment"].sum()
    else:
        # unknown investment -> use current value as proxy
        investment = (last_close * last[shares_col]).sum() if shares_col in last.columns else (last_close).sum()

    current_value = (last_close * last.get(shares_col, 1)).sum()
    total_gain = current_value - investment

    top_holdings = last_close.sort_values(ascending=False).head(5)
    top_df = pd.DataFrame({"Symbol": top_holdings.index, "Latest Close": top_holdings.values})

    summary = [
        {"Metric": "Number of Symbols", "Value": df["Symbol"].nunique()},
        {"Metric": "Current Value (approx.)", "Value": f"{current_value:,.2f}"},
        {"Metric": "Total Gain/Loss (approx.)", "Value": f"{total_gain:,.2f}"},
    ]
    summary_df = pd.DataFrame(summary)
    return summary_df

def performance_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    if df.empty or "Symbol" not in df.columns:
        return pd.DataFrame({"Metric": ["Error"], "Value": ["No data / missing Symbol column"]})
    # compute daily returns per symbol
    df_sorted = df.sort_values(["Symbol", "Date"])
    # ensure index is datetime
    if "Date" in df.columns:
        df_sorted["Date"] = pd.to_datetime(df_sorted["Date"])
    # pivot to have Close per symbol as columns
    pivot = df_sorted.pivot(index="Date", columns="Symbol", values="Close")
    # daily pct change
    daily_ret = pivot.pct_change().dropna(how="all")
    # aggregated metrics
    metrics = []
    for sym in pivot.columns:
        series = pivot[sym].dropna()
        if series.empty:
            continue
        total_return = (series.iloc[-1] / series.iloc[0]) - 1
        annualized = (1 + total_return) ** (365 / max(1, (series.index[-1] - series.index[0]).days)) - 1
        vol = daily_ret[sym].std() * (252 ** 0.5) if sym in daily_ret else np.nan
        metrics.append({"Symbol": sym, "Total Return": f"{total_return:.2%}", "Annualized (est.)": f"{annualized:.2%}", "Volatility (est.)": f"{vol:.2%}" if not np.isnan(vol) else "N/A"})
    return pd.DataFrame(metrics)
