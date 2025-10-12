<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/featureImage.png" alt="Logo">

**# StockAnalysis 💬 **

A simple Streamlit app that shows how to build a AI Powered StockAnalysis for DataU Capstone project. We basically can get data running directly on python, yet we decided to go through ETL CSV to Database, to Power BI all the way to streamlit app. 
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

**✨ Features **

```
🔗 SQL Server integration: Pulls stock data directly from your database (stock_prices_Ver2 table).

📈 Candlestick charts with overlays: SMA50, SMA200, EMA20, Bollinger Bands.

📊 Indicators: RSI14, MACD (12,26,9).

🚦 Signal detection: Golden/Death cross, RSI overbought/oversold, MACD crossovers.

🔮 Forecasting: 12‑month Prophet forecast with confidence intervals.

💰 Scenario simulator: Enter an investment amount and see expected value in 3m, 6m, 12m.

🔄 Trade suggestions: Highlights potential sell/buyback points from forecast peaks/troughs.
```

**Technologies used:**
```
1. SSIS
2. SQL
3. Power BI
4. Python
 4.1 Streamlit
 4.2 Prophet
 4.3 yfinance

```
**## How to run it on your own machine**

**#1. Setup ETL Flow on SSIS**

Beware that our data is store in SQL Service on local marchine to illustrate ETL technique with SSIS that we've learn in DataU. 
<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/ETL.png" alt="Logo">

Create py (Python) file store in your project folder with following script to download data to your computer. In our case, we put this file in ETL folder and name it "extractStockDataVER2.py". 

```
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
```
Then in SSIS run the script by use Execute Process Tast to load the file and run. 
<img width="953" height="638" alt="image" src="https://github.com/user-attachments/assets/48803e62-e8c4-4146-9c00-3e99c96fcc7b" />

Now we get the CSV files store in our download folder destination. 
<img width="682" height="986" alt="image" src="https://github.com/user-attachments/assets/3d17497d-c866-4283-a2b5-c113ad090939" />

Let's Performance loading data to staging data base. Now we need a staging database. Go to SSMS create a staging table with following script. A copy of this SQL script is available in ETL folder, named ". 

```
USE master;
Go
DROP DATABASE IF EXISTS stock_db_staging;
Go
CREATE DATABASE stock_db_staging
ON
(
NAME = stock_db_staging,
FILENAME = 'D:\SQLdata\StockDB_staging.mdf',
SIZE = 10MB,
MAXSIZE = 100MB,
FILEGROWTH = 10MB
)
LOG ON
(
NAME = stock_db_staging_log,
FILENAME = 'D:\SQLdata\StockDB_staging_Log.ldf',
SIZE = 5MB,
MAXSIZE = 50MB,
FILEGROWTH = 5MB);
Go

USE stock_db_staging;
Go

CREATE TABLE stock_prices_staging_Ver2 (
    [Date]            VARCHAR(50),
    [Open]            VARCHAR(50),
    [High]            VARCHAR(50),
    [Low]             VARCHAR(50),
    [Close]           VARCHAR(50),
    [Volume]          VARCHAR(50),
    [Dividends]       VARCHAR(50),
    [Stock_Splits]    VARCHAR(50),
    [SMA50]           VARCHAR(50),
    SMA200          VARCHAR(50),
    EMA20           VARCHAR(50),
    RSI14           VARCHAR(50),
    MACD            VARCHAR(50),
    MACD_Signal     VARCHAR(50),
    MACD_Hist       VARCHAR(50),
    BB_Mid          VARCHAR(50),
    BB_Upper        VARCHAR(50),
    BB_Lower        VARCHAR(50),
    Ticker          VARCHAR(20)
);

```
<img width="1915" height="1026" alt="image" src="https://github.com/user-attachments/assets/b08399a5-c084-4b1f-8288-9bc811c005ca" />

Now load the data from CSV Files to staging database with this Forloop setup. In this step we keep the same data type as it on CSV file.
<img width="1909" height="1024" alt="image" src="https://github.com/user-attachments/assets/49499bc8-0f41-4518-adae-c1e9f476aecd" />

After complete loading data to staging database, the CSV files are move to achieve folder using "File System Task". 
<img width="1366" height="950" alt="image" src="https://github.com/user-attachments/assets/2449d609-685d-4b31-98a9-a8a8a0f89e8e" />

Last step on ETL stage, is getting data from staging database to Data Warehouse (DWH). 
Now we need to create database for DWH. Run the SQL script below in SSMS to create Database for DWH.

```
USE master;
Go
DROP DATABASE IF EXISTS stock_db;
Go
CREATE DATABASE stock_db
ON
(
NAME = stock_db,
FILENAME = 'D:\SQLdata\StockDB.mdf',
SIZE = 10MB,
MAXSIZE = 100MB,
FILEGROWTH = 10MB
)
LOG ON
(
NAME = stock_db_log,
FILENAME = 'D:\SQLdata\StockDB_Log.ldf',
SIZE = 5MB,
MAXSIZE = 50MB,
FILEGROWTH = 5MB);
Go

USE stock_db;
Go
Drop Table IF EXISTS dbo.stock_prices_Ver2;
-- Stock Prices Ver2
CREATE TABLE stock_prices_Ver2 (
    Price_ID        INT IDENTITY(1,1) PRIMARY KEY,  -- surrogate key
    Ticker          VARCHAR(20) NOT NULL,
    Price_Date      DATE NOT NULL,
    [Open]            DECIMAL(18,4),
    [High]            DECIMAL(18,4),
    [Low]             DECIMAL(18,4),
    [Close]           DECIMAL(18,4),
    Volume          BIGINT,
    Dividends       DECIMAL(18,4),
    Stock_Splits    DECIMAL(18,4),

    -- Technical Indicators
    SMA50           DECIMAL(18,4) Null,
    SMA200          DECIMAL(18,4) Null,
    EMA20           DECIMAL(18,4) Null,
    RSI14           DECIMAL(10,4) Null,
    MACD            DECIMAL(18,4) Null,
    MACD_Signal     DECIMAL(18,4) Null,
    MACD_Hist       DECIMAL(18,4) Null,
    BB_Mid          DECIMAL(18,4) Null,
    BB_Upper        DECIMAL(18,4) Null,
    BB_Lower        DECIMAL(18,4) Null,

    -- Index
    CONSTRAINT uq_stock UNIQUE (Ticker, Price_Date)
);
```
Setup Flow to load data from staging to DWH. On this stage, we need to meonipolate data before we load to DWH. 
<img width="1912" height="1025" alt="image" src="https://github.com/user-attachments/assets/db1a4d44-2a43-49cb-9765-9c477356393d" />

A Derived Column task were used to convert null data. 
<img width="815" height="647" alt="image" src="https://github.com/user-attachments/assets/748296ed-fb4f-4893-ba13-4530199e4bbb" />
Then Convert data types. 
<img width="992" height="840" alt="image" src="https://github.com/user-attachments/assets/31aeaa3a-7cfb-49e2-89ac-22996a00f93d" />
To avoid loading repeat data, duplicate to existing rows, we load only data that doesn't match in this Lookup to DWH. 
<img width="1003" height="652" alt="image" src="https://github.com/user-attachments/assets/14e14089-9974-4acd-8627-909c12b67623" />

**The ETL Step is completed.**

**#2. 🛠️ Installation (Local Machine)**
```
git clone https://github.com/hempiden/StockAnalysis.git
cd StockAnalysis
```

**#3 pip install -r requirements.txt**

```
pip install -r requirements.txt
```

  **Requirement.txt list:**
  
  ```
  streamlit
  pandas
  pyodbc
  plotly
  prophet
  numpy
  scipy
  ```

**#4 Configure SQL Server connection**

Edit app.py and update:
```
SERVER = "YOUR_SERVER_NAME"
DATABASE = "stock_db"
DRIVER = "ODBC Driver 17 for SQL Server"
TABLE = "[dbo].[stock_prices_Ver2]"
```

**Make sure:**

  1. SQL Server is running and accessible.
  2. You replace with the info of your server, database and table.
  3. You have the correct ODBC driver installed (ODBC Driver 17 for SQL Server).

**#5. Run the app**

```
streamlit run app.py
```
Then open the local URL (usually http://localhost:8501) in your browser.

A Power BI Dashboard were also design for project showcase
<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/powerBI.png" alt="Logo">

**Refference**
___

<b>Our inspiration of PowerBI dashboard: <a href="https://community.fabric.microsoft.com/t5/Themes-Gallery/Stock-Market-Technical-Analysis/m-p/3706231">here</a>.</b>
___
