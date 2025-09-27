<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/featureImage.png" alt="Logo">
# StockAnalysis 💬 

A simple Streamlit app that shows how to build a AI Powered StockAnalysis for DataU Capstone project. We basically can get data running directly on python, yet we decided to go through ETL CSV to Database, to Power BI all the way to streamlit app. 
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

#✨ Features Technologies used:

```
🔗 SQL Server integration: Pulls stock data directly from your database (stock_prices_Ver2 table).

📈 Candlestick charts with overlays: SMA50, SMA200, EMA20, Bollinger Bands.

📊 Indicators: RSI14, MACD (12,26,9).

🚦 Signal detection: Golden/Death cross, RSI overbought/oversold, MACD crossovers.

🔮 Forecasting: 12‑month Prophet forecast with confidence intervals.

💰 Scenario simulator: Enter an investment amount and see expected value in 3m, 6m, 12m.

🔄 Trade suggestions: Highlights potential sell/buyback points from forecast peaks/troughs.
```
### How to run it on your own machine
#1. 🛠️ Installation (Local Machine)
```
git clone https://github.com/hempiden/StockAnalysis.git
cd stock-analysis-dashboard
```
#2 pip install -r requirements.txt 
```
pip install -r requirements.txt
```
  Requirement.txt list:
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

Beware that our data is store in SQL Service on local marchine to illustrate ETL technique with SSIS
<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/ETL.png" alt="Logo">

A Power BI Dashboard were also design for project showcase
<img src="https://github.com/hempiden/StockAnalysis/blob/main/.streamlit/powerBI.png" alt="Logo">
