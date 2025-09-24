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

-- Prices with indicators
CREATE TABLE stock_prices_staging (
    Ticker VARCHAR(10),
    [date] DATE,
    [open] DECIMAL(15,4),
    [high] DECIMAL(15,4),
    [low] DECIMAL(15,4),
    [close] DECIMAL(15,4),
    volume BIGINT,	
	[split] DECIMAL(15,4),
	[Dividends] DECIMAL(15,4),
);

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
