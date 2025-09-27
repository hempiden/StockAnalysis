import pyodbc
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import date, timedelta
from prophet import Prophet
import numpy as np
from scipy.signal import argrelextrema

# ---------- Settings ----------
SERVER = "DESKTOP-6EGKSS9"
DATABASE = "stock_db"
DRIVER = "ODBC Driver 17 for SQL Server"
TABLE = "[dbo].[stock_prices_Ver2]"

def get_conn():
    conn_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

# ---------- Page config ----------
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
st.title("📊 Stock Analysis Dashboard")
st.caption("SQL Server + Streamlit + Plotly + Prophet")

# ---------- Data loader ----------
@st.cache_data(show_spinner=True)
def load_tickers():
    with get_conn() as conn:
        q = f"SELECT DISTINCT Ticker FROM {TABLE} ORDER BY Ticker;"
        return pd.read_sql(q, conn)["Ticker"].tolist()

@st.cache_data(show_spinner=True)
def load_data(ticker: str, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    q = f"""
    SELECT
        [Price_Date] AS [Date],
        [Open], [High], [Low], [Close], [Volume], [Ticker],
        [SMA50], [SMA200], [EMA20],
        [RSI14],
        [MACD], [MACD_Signal], [MACD_Hist],
        [BB_Mid], [BB_Upper], [BB_Lower]
    FROM {TABLE}
    WHERE [Ticker] = ? AND [Price_Date] >= ? AND [Price_Date] <= ?
    ORDER BY [Price_Date]
    """
    with get_conn() as conn:
        df = pd.read_sql(q, conn, params=[ticker, start, end])
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# ---------- Forecast helpers ----------
@st.cache_data(show_spinner=True)
def forecast_price(df: pd.DataFrame, periods: int = 365) -> pd.DataFrame:
    # Prophet expects ds (date) and y (value)
    prophet_df = df[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet(daily_seasonality=False, yearly_seasonality=True)
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast

def find_trade_points(forecast: pd.DataFrame, order: int = 30):
    prices = forecast["yhat"].values
    maxima_idx = argrelextrema(prices, np.greater, order=order)[0]
    minima_idx = argrelextrema(prices, np.less, order=order)[0]
    maxima = forecast.iloc[maxima_idx]
    minima = forecast.iloc[minima_idx]
    return maxima, minima

# ---------- Sidebar controls ----------
with st.sidebar:
    st.header("Controls")
    tickers = load_tickers()
    selected_ticker = st.selectbox("Ticker", tickers, index=0 if tickers else None)

    today = date.today()
    default_start = today - timedelta(days=365)
    start_date = st.date_input("Start date", value=default_start)
    end_date = st.date_input("End date", value=today)

    show_sma50 = st.checkbox("Show SMA50", value=True)
    show_sma200 = st.checkbox("Show SMA200", value=True)
    show_ema20 = st.checkbox("Show EMA20", value=False)
    show_bbands = st.checkbox("Show Bollinger Bands", value=False)
    show_volume = st.checkbox("Show Volume", value=True)

    st.markdown("---")
    show_rsi = st.checkbox("Show RSI (14)", value=True)
    show_macd = st.checkbox("Show MACD (12,26,9)", value=True)

# ---------- Load data ----------
if not selected_ticker:
    st.warning("No tickers found. Check your database and table.")
    st.stop()

df = load_data(selected_ticker, pd.Timestamp(start_date), pd.Timestamp(end_date))
if df.empty:
    st.warning("No data for selected range/ticker.")
    st.stop()

# ---------- Tabs ----------
price_tab, indicators_tab, signals_tab, forecast_tab = st.tabs(
    ["Price & overlays", "Indicators", "Signals", "Forecast & Strategy"]
)

# ---------- Price chart ----------
with price_tab:
    st.subheader(f"Price chart — {selected_ticker}")
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["Date"], open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name="OHLC",
        increasing_line_color="#26a69a", decreasing_line_color="#ef5350"
    ))

    if show_sma50 and "SMA50" in df:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["SMA50"], name="SMA50"))
    if show_sma200 and "SMA200" in df:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["SMA200"], name="SMA200"))
    if show_ema20 and "EMA20" in df:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["EMA20"], name="EMA20"))
    if show_bbands and {"BB_Upper","BB_Lower"}.issubset(df.columns):
        fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Upper"], name="BB Upper", line=dict(color="gray")))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Lower"], name="BB Lower", line=dict(color="gray")))

    fig.update_layout(height=600, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    if show_volume and "Volume" in df:
        st.subheader("Volume")
        vfig = go.Figure()
        vfig.add_trace(go.Bar(x=df["Date"], y=df["Volume"], name="Volume", marker_color="#90caf9"))
        vfig.update_layout(height=200)
        st.plotly_chart(vfig, use_container_width=True)

# ---------- Indicators ----------
with indicators_tab:
    col1, col2 = st.columns(2)

    with col1:
        if show_rsi and "RSI14" in df:
            st.subheader("RSI14")
            rsi_fig = go.Figure()
            rsi_fig.add_trace(go.Scatter(x=df["Date"], y=df["RSI14"], name="RSI14"))
            rsi_fig.add_hline(y=70, line_dash="dot", line_color="red")
            rsi_fig.add_hline(y=30, line_dash="dot", line_color="green")
            rsi_fig.update_layout(height=250)
            st.plotly_chart(rsi_fig, use_container_width=True)

    with col2:
        if show_macd and {"MACD","MACD_Signal","MACD_Hist"}.issubset(df.columns):
            st.subheader("MACD")
            macd_fig = go.Figure()
            macd_fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD"], name="MACD"))
            macd_fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD_Signal"], name="Signal"))
            macd_fig.add_trace(go.Bar(x=df["Date"], y=df["MACD_Hist"], name="Hist"))
            macd_fig.update_layout(height=250)
            st.plotly_chart(macd_fig, use_container_width=True)

# ---------- Signals ----------
with signals_tab:
    st.subheader("Basic signals")
    sigs = []

    # SMA crossovers
    if {"SMA50","SMA200"}.issubset(df.columns) and len(df) >= 2:
        prev, last = df.iloc[-2], df.iloc[-1]
        if pd.notna(prev["SMA50"]) and pd.notna(prev["SMA200"]) and pd.notna(last["SMA50"]) and pd.notna(last["SMA200"]):
            if prev["SMA50"] < prev["SMA200"] and last["SMA50"] > last["SMA200"]:
                sigs.append("Golden cross (SMA50 crossed above SMA200)")
            elif prev["SMA50"] > prev["SMA200"] and last["SMA50"] < last["SMA200"]:
                sigs.append("Death cross (SMA50 crossed below SMA200)")

    # RSI levels
    if "RSI14" in df and not df["RSI14"].isna().all():
        rsi_last = df["RSI14"].dropna().iloc[-1]
        if rsi_last >= 70:
            sigs.append(f"RSI overbought ({rsi_last:.1f})")
        elif rsi_last <= 30:
            sigs.append(f"RSI oversold ({rsi_last:.1f})")

    # MACD crossovers
    if {"MACD","MACD_Signal"}.issubset(df.columns):
        macd_prev = df[["MACD","MACD_Signal"]].dropna().iloc[-2:]
        if len(macd_prev) == 2:
            a1, b1 = macd_prev.iloc[0]["MACD"], macd_prev.iloc[0]["MACD_Signal"]
            a2, b2 = macd_prev.iloc[1]["MACD"], macd_prev.iloc[1]["MACD_Signal"]
            if a1 < b1 and a2 > b2:
                sigs.append("MACD bullish crossover")
            elif a1 > b1 and a2 < b2:
                sigs.append("MACD bearish crossover")

    if sigs:
        for s in sigs:
            st.success(f"• {s}")
    else:
        st.info("No signals detected.")

# ---------- Forecast & Strategy ----------
with forecast_tab:
    st.subheader(f"Forecast & Strategy — {selected_ticker}")

    # Forecast 1 year ahead
    forecast = forecast_price(df, periods=365)

    # Plot forecast
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="Historical"))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], name="Forecast"))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"],
                             name="Upper", line=dict(dash="dot", color="gray")))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"],
                             name="Lower", line=dict(dash="dot", color="gray")))
    fig.update_layout(height=500, xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

    # Expected returns
    today_price = df["Close"].iloc[-1]
    horizons = {"3m": 90, "6m": 180, "12m": 365}
    st.subheader("📈 Expected Returns if Entering Now")
    for label, days in horizons.items():
        if len(forecast) > days:
            future_price = forecast.iloc[-days]["yhat"]
            ret = (future_price - today_price) / today_price * 100
            st.metric(label=f"{label} return", value=f"{ret:.2f}%")

    # Scenario simulator
    st.subheader("💰 Investment Scenario Simulator")
    investment = st.number_input("Enter investment amount ($)", min_value=100, value=10000, step=100)

    results = []
    for label, days in horizons.items():
        if len(forecast) > days:
            future_price = forecast.iloc[-days]["yhat"]
            ret_pct = (future_price - today_price) / today_price * 100
            future_value = investment * (1 + ret_pct / 100)
            results.append((label, f"{ret_pct:.2f}%", f"${future_value:,.2f}"))

    if results:
        st.table(pd.DataFrame(results, columns=["Horizon", "Expected Return", "Estimated Value"]))

    # Suggested trade points
    st.subheader("🔄 Potential Sell/Buyback Points")
    maxima, minima = find_trade_points(forecast)
    if not maxima.empty:
        st.write("📈 Suggested Sell Dates:")
        st.dataframe(maxima[["ds", "yhat"]].rename(columns={"ds": "Date", "yhat": "Price"}))
    if not minima.empty:
        st.write("📉 Suggested Buyback Dates:")
        st.dataframe(minima[["ds", "yhat"]].rename(columns={"ds": "Date", "yhat": "Price"}))

# ---------- Data preview ----------
st.markdown("---")
st.subheader("Data preview")
st.dataframe(df.tail(200), use_container_width=True)
