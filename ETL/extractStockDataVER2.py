import yfinance as yf
import pandas as pd
import os

# === Settings ===
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "NFLX", "AMD", "INTC",
    "IBM", "ORCL", "CRM", "ADBE", "CSCO", "QCOM", "AVGO", "TXN", "PYPL", "SHOP",
    "BA", "NKE", "DIS", "PEP", "KO", "MCD", "WMT", "OPEN", "SMCI", "PAYO", "SOFI",
    "UPS", "SBUX", "CMCSA", "F", "HNST", "PLTR"
]

period = "3y"

# Create output folder
output_dir = "stock_data_csv"
os.makedirs(output_dir, exist_ok=True)

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.clip(lower=0, upper=100)

def add_technical_indicators(df, ticker):
    df = df.copy()

    # Moving Averages
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

    # RSI
    df["RSI14"] = compute_rsi(df["Close"], 14)

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]

    # Bollinger Bands
    df["BB_Mid"] = df["Close"].rolling(window=20).mean()
    df["BB_Upper"] = df["BB_Mid"] + 2 * df["Close"].rolling(window=20).std()
    df["BB_Lower"] = df["BB_Mid"] - 2 * df["Close"].rolling(window=20).std()

    df["Ticker"] = ticker
    return df

# === Download loop ===
for t in tickers:
    print(f"Downloading {t}...")
    stock = yf.Ticker(t)
    hist = stock.history(period=period)
    hist = add_technical_indicators(hist, t)
    hist.to_csv(f"{output_dir}/{t}_prices.csv")

print("✅ All data + indicators downloaded into 'stock_data_csv/' folder")
