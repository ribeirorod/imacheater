# SQL cheat sheet - My most common commands


### Execution ORDER

FROM, JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT, OFFSET

CASE is faster than JOINS


### TABLE / VIEW Manipulation

```sql

```

### CTEs
```sql
```

### GROUPING
```sql
```

### SUBQUERIES
```sql
```

### DIFFEREN CASE USES
```sql
```

### JOINS (IF you cant fit CASE)



### TIME COMPARISION - YESTERDAYs 


## Self JOIN
```sql
# self-join
SELECT w1.id AS id
FROM Weather w1
LEFT JOIN Weather w2
ON DATEDIFF(w1.recordDate,w2.recordDate) =1
WHERE w1.Temperature > w2.Temperature
```

```sql
SELECT
  Name
  ,Code
  ,Continent
  ,Population
FROM country
WHERE (Continent, Population) IN (
  SELECT
    a.Continent
    ,MAX(a.Population) AS Population
  FROM country AS a 
  GROUP BY a.Continent
);
```

```sql
SELECT
  CountryCode
  ,COUNT(*) AS city_tally
FROM city
GROUP BY CountryCode
HAVING city_tally >= 100
ORDER BY city_tally DESC;
```

## Window Functions

```sql
-- running total on entire data
SELECT duration_seconds,
       SUM(duration_seconds) OVER (ORDER BY start_time) AS running_total
FROM tutorial.dc_bikeshare_q1_2012

--narrowed by individual groups using PARTITION BY
--ORDER BY, orders the designated column(s) the same way, except that it treats every partition as separate.
SELECT start_terminal,
       duration_seconds,
       SUM(duration_seconds) OVER
         (PARTITION BY start_terminal ORDER BY start_time)
         AS running_total
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08'


--ROW_NUMBER()displays the number of a given row. It starts are 1 and numbers the rows according to the ORDER BY part of the window statement.
SELECT start_terminal,
       start_time,
       duration_seconds,
       ROW_NUMBER() OVER (PARTITION BY start_terminal
                          ORDER BY start_time)
                    AS row_number
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08'

 -- Other functions RANK |DESNE_RANK |NTILE |LAG |LEAD

-- Difference between ROWS
 SELECT start_terminal,
       duration_seconds,
       duration_seconds - LAG(duration_seconds, 1) OVER
         (PARTITION BY start_terminal ORDER BY duration_seconds)
         AS difference
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08'
 ORDER BY start_terminal, duration_seconds


--Define Window ALIAS 
--WINDOW clause, if included, should always come after the WHERE clause
SELECT start_terminal,
       duration_seconds,
       NTILE(4)   OVER ntile_window AS quartile,
       NTILE(5)   OVER ntile_window AS quintile,
       NTILE(100) OVER ntile_window AS percentile
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08'

WINDOW ntile_window AS
         (PARTITION BY start_terminal ORDER BY duration_seconds)
 ORDER BY start_terminal, duration_seconds

```

```sql



SELECT 
  C_NAME as customer_name,
  N_NAME as nation_name,
  MAX(O_ORDERAMOUNT) as total_spend_amount
FROM 
  CUSTOMER C
  LEFT JOIN NATION N ON C.NATIONKEY = N.N_NATIONKEY
  LEFT JOIN (SELECT O_ORDERAMOUNT FROM ORDER WHERE ORDERSTATUS=''COMPLETED) O ON C. = O.O_CUSKEY
GROUPY BY 
  customer_name, nation_name




SELECT 
  C.C_NAME AS CUSTOMER_NAME, 
  N.N_NAME AS NATION_NAME,
  MAX(O.O_ORDERAMOUNT) AS MAXVALUE
FROM 
  CUSTOMER C
  LEFT JOIN NATION ON (C.NATIONKEY = N.N_NATIONKEY)
  INNER JOIN (SELECT O_ORDERAMOUNT FROM ORDERS WHERE O_ORDERSTATUS = 'COMPLETE') O ON (C.CUSKEY = O.CUSKEY)
ORDER BY MAXVALUE DESC
GROUP BY NATION_NAME, CUSTOMER_NAME

```