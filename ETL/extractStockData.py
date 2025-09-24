import yfinance as yf
import pandas as pd
import os

# === Settings ===
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "NFLX", "AMD", "INTC", 
"IBM", "ORCL", "CRM", "ADBE", "CSCO", "QCOM", "AVGO", "TXN", "PYPL", "SHOP", 
"BA", "NKE", "DIS", "PEP", "KO", "MCD", "WMT", "OPEN", "SMCI", "PAYO", "SOFI", "UPS", "SBUX", "CMCSA", "F", "HNST", "PLTR"
]   # 👈 add more tickers here
period = "3y"  # e.g. "1y", "3y", "5y", "max"

# Create output folder
output_dir = "stock_data_csv"
os.makedirs(output_dir, exist_ok=True)

def add_technical_indicators(df, ticker):
    df = df.copy()

    # # Simple Moving Averages
    # df["SMA50"] = df["Close"].rolling(window=50).mean()
    # df["SMA200"] = df["Close"].rolling(window=200).mean()

    # # Exponential Moving Average
    # df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

    # # Relative Strength Index (RSI 14)
    # delta = df["Close"].diff()
    # gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    # loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    # rs = gain / loss
    # df["RSI14"] = 100 - (100 / (1 + rs))

    # # MACD (12, 26, 9)
    # ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    # ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    # df["MACD"] = ema12 - ema26
    # df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    # df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]

    # # Bollinger Bands (20, 2σ)
    # df["BB_Mid"] = df["Close"].rolling(window=20).mean()
    # df["BB_Upper"] = df["BB_Mid"] + 2 * df["Close"].rolling(window=20).std()
    # df["BB_Lower"] = df["BB_Mid"] - 2 * df["Close"].rolling(window=20).std()

    # Add ticker column
    df["Ticker"] = ticker  

    return df

for t in tickers:
    print(f"Downloading {t}...")

    stock = yf.Ticker(t)

    # 1. Historical OHLCV + Indicators
    hist = stock.history(period=period)
    hist = add_technical_indicators(hist, t)
    hist.to_csv(f"{output_dir}/{t}_prices.csv")

print("✅ All data + indicators downloaded into 'stock_data_csv/' folder")