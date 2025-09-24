
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