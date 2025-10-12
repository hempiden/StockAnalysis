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


Drop Table IF EXISTS dbo.stock_prices_Ver2 ;
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
