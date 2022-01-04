# SQL cheat sheet - My most common commands



### Execution ORDER


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