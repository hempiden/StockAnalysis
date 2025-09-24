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

-- Users
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- Requests (logs user activity + recommendation results)
CREATE TABLE dbo.requests(
    request_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    interval VARCHAR(10) NOT NULL,
    recommendation NVARCHAR(MAX),
    request_time DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Stock Prices
CREATE TABLE dbo.stock_prices(
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    [date] DATE NOT NULL,
    [open] DECIMAL(15,4),
    [high] DECIMAL(15,4),
    [low] DECIMAL(15,4),
    [close] DECIMAL(15,4),
    volume BIGINT,
	[split] DECIMAL(15,4),
	[Dividends] DECIMAL(15,4),
	CONSTRAINT uq_stock_date UNIQUE (ticker, [date])
);

Drop table dbo.stock_prices_Ver2 ;
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