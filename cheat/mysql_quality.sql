

SELECT COUNT(*) AS row_count
FROM mytable

-- Min/max/avg and more for numbers & dates

SELECT MIN(mycolumn) AS value_min, 
       MAX(mycolumn) AS value_max, 
       AVG(mycolumn) AS value_avg, 
       STDEV(mycolumn) AS value_stddev, 
       VAR(mycolumn) AS value_var
FROM mytable
WHERE mycolumn IS NOT NULL

-- MIN MAX STRING

SELECT MIN(mycolumn) AS value_min_string, 
       MAX(mycolumn) AS value_max_string
FROM mytable
WHERE mycolumn IS NOT NULL
AND LEN(mycolumn) > 0

-- TEST RANGE
DECLARE 
@min int = 10,
@max int = 200;   

SELECT 
    SUM(CASE WHEN mycolumn < @min THEN 1 ELSE 0 end) AS below_range,
    SUM(CASE WHEN mycolumn BETWEEN @min and @max THEN 1 ELSE 0 end) AS within_range,
    SUM(CASE WHEN mycolumn > @max THEN 1 ELSE 0 end) AS above_range
FROM mytable

-- LEN Distribution

SELECT LEN(mycolumn) AS string_length,
       count(*) AS row_count
FROM mytable
GROUP BY LEN(mycolumn)
ORDER BY 1

--  TOP Values 

SELECT TOP 10
    mycolumn AS value, 
    COUNT(*) row_count
from mytable
WHERE mycolumn IS NOT null
GROUP BY mycolumn
ORDER BY COUNT(*) desc

-- Random Rows

SELECT * 
FROM mytable
WHERE id IN (
    SELECT TOP (10) id
    FROM mytable
    ORDER BY NEWID())

SELECT 
    customerNumber, 
    customerName
FROM
    customers
ORDER BY RAND()
LIMIT 5;

-- NULL ROWS

SELECT row_type,
    COUNT(*) row_count
FROM 
    (SELECT 
        CASE WHEN mycolumn IS NULL THEN 'Null'
            ELSE 'Non Empty' 
            END AS row_type
        FROM mytable) rows
GROUP BY row_type

-- NULLS EMPTY
SELECT row_type,
    COUNT(*) row_count
FROM 
    (SELECT 
        CASE WHEN mycolumn IS NULL THEN 'Null'
            WHEN LEN(mycolumn) = 0 THEN 'Empty'
            ELSE 'Non Empty' 
            END AS row_type
        FROM mytable) rows
GROUP BY row_type

-- TEST UNIQUENESS

SELECT row_type, 
    SUM(row_count) AS row_count
FROM
    (SELECT 
        CASE WHEN [value] IS NULL then 'NULL'
            WHEN row_count = 1 then 'Unique'
            ELSE 'Non Unique' 
            END AS row_type,
        row_count
    FROM (
        SELECT mycolumn [value], 
            COUNT(*) row_count
        FROM mytable
        GROUP BY mycolumn) X) Y
GROUP BY row_type

-- TEST ORPHANED ROWS - FORERIGN KEYS
SELECT 
    fk.foreignkey, 
    COUNT(*) orphaned_rows
FROM foreigntable fk
    LEFT OUTER JOIN primarytable pk
        ON fk.foreignkey = pk.primarykey
WHERE pk.primarykey IS NULL
GROUP BY fk.foreignkey
ORDER BY 2 DESC


SET @tbl_name =`mytable`
SET @ID_1 = (SELECT ID FROM `slider` LIMIT 0,1);
SET @Cat = (SELECT Category FROM `slider` LIMIT 0,1);

SET @sql = CONCAT('select * from ', @Cat, ' where ID = ', @ID_1); 

PREPARE stmt FROM @sql; 
EXECUTE stmt; 