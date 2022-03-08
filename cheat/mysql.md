
### ORDER of Execution

FROM, JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT, OFFSET


# Creating Tables

```sql

CREATE TEMPORARY TABLE db_name.tbl_name
CREATE TABLE IF NOT EXISTS db_name.tbl_name
CREATE TABLE IF NOT EXISTS db_name.tbl_name LIKE old_tbl_name

CREATE TABLE t (c CHAR(20) CHARACTER SET utf8 COLLATE utf8_bin);

CREATE TABLE t1 (
    c1 INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    c2 VARCHAR(100),
    c3 VARCHAR(100) )

CREATE TABLE test (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (a), 
    KEY(b))
    ENGINE=InnoDB SELECT b,c FROM test2;

CREATE TABLE tv1
    SELECT * FROM (VALUES ROW(1,3,5), ROW(2,4,6)) AS v;

CREATE TABLE tv2 (a INT, b INT, c INT)
    SELECT * FROM (VALUES ROW(1,3,5), ROW(2,4,6)) AS v(a,b,c);

```

# Creating Indexes
Most MySQL indexes (PRIMARY KEY, UNIQUE, INDEX, and FULLTEXT) are stored in B-trees.

```sql
CREATE TABLE t1 (
  col1 VARCHAR(10),
  col2 VARCHAR(20),
  INDEX (col1, col2(10))
);
```

Use of functional key parts enables indexing of values not stored directly in the table. Examples:

```sql

CREATE TABLE t1 (col1 INT, col2 INT, INDEX func_index ((ABS(col1))));

CREATE INDEX idx1 ON t1 ((col1 + col2));
CREATE INDEX idx2 ON t1 ((col1 + col2), (col1 - col2), col1);

ALTER TABLE t1 ADD INDEX ((col1 * 40) DESC);
```

# Setting PRIMARY and FOREIGN KEYS
 CREATE INDEX cannot be used to create a PRIMARY KEY; use ALTER TABLE instead


```sql
CREATE TABLE Persons (
    ID int NOT NULL PRIMARY KEY,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    OrdersId int FOREIGN KEY REFERENCES Orders(ID)
    
);

CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    CONSTRAINT PK_Person PRIMARY KEY (ID,LastName)
);

ALTER TABLE Persons
ADD [DROP] PRIMARY KEY (ID);

ALTER TABLE Persons
ADD [DROP] CONSTRAINT PK_Person PRIMARY KEY (ID,LastName);
```


# Partitioning

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5))
    PARTITION BY HASH(col1);

CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATETIME)
    PARTITION BY HASH ( YEAR(col3) );

CREATE TABLE tk (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY LINEAR KEY(col3)
    PARTITIONS 5;



CREATE TABLE t1 (
    year_col  INT,
    some_data INT
)
PARTITION BY RANGE (year_col) (
    PARTITION p0 VALUES LESS THAN (1991),
    PARTITION p1 VALUES LESS THAN (1995),
    PARTITION p2 VALUES LESS THAN (1999),
    PARTITION p3 VALUES LESS THAN (2002),
    PARTITION p4 VALUES LESS THAN (2006),
    PARTITION p5 VALUES LESS THAN MAXVALUE
);

CREATE TABLE rc (
    a INT NOT NULL,
    b INT NOT NULL
)
PARTITION BY RANGE COLUMNS(a,b) (
    PARTITION p0 VALUES LESS THAN (10,5),
    PARTITION p1 VALUES LESS THAN (20,10),
    PARTITION p2 VALUES LESS THAN (50,MAXVALUE),
    PARTITION p3 VALUES LESS THAN (65,MAXVALUE),
    PARTITION p4 VALUES LESS THAN (MAXVALUE,MAXVALUE)
);

CREATE TABLE client_firms (
    id   INT,
    name VARCHAR(35)
)
PARTITION BY LIST (id) (
    PARTITION r0 VALUES IN (1, 5, 9, 13, 17, 21),
    PARTITION r1 VALUES IN (2, 6, 10, 14, 18, 22),
    PARTITION r2 VALUES IN (3, 7, 11, 15, 19, 23),
    PARTITION r3 VALUES IN (4, 8, 12, 16, 20, 24)
);

CREATE TABLE lc (
    a INT NULL,
    b INT NULL
)
PARTITION BY LIST COLUMNS(a,b) (
    PARTITION p0 VALUES IN( (0,0), (NULL,NULL) ),
    PARTITION p1 VALUES IN( (0,1), (0,2), (0,3), (1,1), (1,2) ),
    PARTITION p2 VALUES IN( (1,0), (2,0), (2,1), (3,0), (3,1) ),
    PARTITION p3 VALUES IN( (1,3), (2,2), (2,3), (3,2), (3,3) )
);

```
## Clustered Index

## Column Index 

# Performance Enhancement

For comparisons between nonbinary string columns, both columns should use the same character set. For example, comparing a utf8 column with a latin1 column precludes use of an index.

## Avoid to USE to escape full table reads:

The table is so small that it is faster to perform a table scan than to bother with a key lookup

There are no usable restrictions in the ON or WHERE clause for indexed columns

You are using a key with low cardinality (many rows match the key value) through another column. In this case, MySQL assumes that by using the key probably requires many key lookups and that a table scan would be faster
- 

Use ANALYZE TABLE tbl_name to update the key distributions for the scanned table.

The FORCE INDEX hint acts like USE INDEX (index_list), with the addition that a table scan is assumed to be very expensive. In other words, a table scan is used only if there is no way to use one of the named indexes to find rows in the table.

```sql
SELECT * FROM table1 USE INDEX (col1_index,col2_index)
  WHERE col1=1 AND col2=2 AND col3=3;

SELECT * FROM table1 IGNORE INDEX (col3_index)
  WHERE col1=1 AND col2=2 AND col3=3;

SELECT * FROM t1 USE INDEX FOR JOIN (i1)

SELECT * FROM t1 IGNORE INDEX (i1)
is equivalent to this combination of hints:

SELECT * FROM t1 IGNORE INDEX FOR JOIN (i1)
SELECT * FROM t1 IGNORE INDEX FOR ORDER BY (i1)
SELECT * FROM t1 IGNORE INDEX FOR GROUP BY (i1)


SELECT * FROM t
  USE INDEX (index1)
  IGNORE INDEX (index1) FOR ORDER BY
  IGNORE INDEX (index1) FOR GROUP BY
  WHERE ... IN BOOLEAN MODE ... ;

SELECT * FROM t
  USE INDEX (index1)
  WHERE ... IN BOOLEAN MODE ... ;

```


# Whats FOREIGN constraints

A foreign key is a column (or combination of columns) in a table whose values must match values of a column in some other table. FOREIGN KEY constraints enforce referential integrity, which essentially says that if column value A refers to column value B, then column value B must exist.