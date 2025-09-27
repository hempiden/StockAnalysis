
truncate table [dbo].[stock_prices_staging];
use stock_db_staging;
Go
select * from  [dbo].[stock_prices_staging];



truncate table [dbo].[stock_prices];
use stock_db;
Go
select * from  [dbo].[stock_prices];

--VER2.0
use stock_db;
Go
truncate table [dbo].[stock_prices_Ver2];


Delete from dbo.stock_prices_Ver2
Where Price_Date ='2025-09-22';


use stock_db;
Go
select * from  [dbo].[stock_prices_Ver2]
Where Price_Date ='2025-09-19';
;

sp_help stock_prices_Ver2


use stock_db_staging;
Go
truncate table [dbo].[stock_prices_staging_Ver2];
use stock_db_staging;
Go
select * from  [dbo].[stock_prices_staging_Ver2];


-- Always good practice: preview the rows before deleting
SELECT *
FROM dbo.stock_prices_Ver2
WHERE Price_Date = '2025-09-26';

-- Once confirmed, run the delete
DELETE FROM dbo.stock_prices_Ver2
WHERE Price_Date = '2025-09-26';



BEGIN TRANSACTION;

DELETE FROM dbo.stock_prices_Ver2
WHERE CAST(price_date AS date) = '2025-09-26';

-- Check how many rows were affected
SELECT @@ROWCOUNT AS RowsDeleted;

-- If correct, commit; otherwise, rollback
-- COMMIT TRANSACTION;
-- ROLLBACK TRANSACTION;
