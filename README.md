<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/featureImage.png" alt="Logo">

**StockAnalysis 💬 **

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
** How to run it on your own machine**


Beware that our data is store in SQL Service on local marchine to illustrate ETL technique with SSIS. Go to Instruction.md for detail instruction from ETL stage. 

<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/ETL.png" alt="Logo">

**#1. 🛠️ Installation (Local Machine)**
```
git clone https://github.com/hempiden/StockAnalysis.git
cd StockAnalysis
```

**#2 pip install -r requirements.txt**

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

**#3 Configure SQL Server connection**

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

**#4. Run the app**

```
streamlit run app.py
```
Then open the local URL (usually http://localhost:8501) in your browser.

**A Power BI Dashboard were also design for project showcase**
<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/powerBI.png" alt="Logo">

**Refference**
___

<b>Our inspiration of PowerBI dashboard: <a href="https://community.fabric.microsoft.com/t5/Themes-Gallery/Stock-Market-Technical-Analysis/m-p/3706231">here</a>.</b>
___
