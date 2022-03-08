
select main.submission_date, main.hackers, main.id, h.name as 'name'
    from 
    (
        select c.submission_date, count(c.hacker_id) as hackers, min(c.hacker_id) as 'id'
        from
        (
            select submission_date, hacker_id , count(submission_id) as 'subs' from submissions
            group by submission_date, hacker_id
        ) as c
        group by c.submission_date
        left join 
        (
            select t2.submission_date , max(t2.subs) as 'maxday'
            from (        
                select submission_date, hacker_id , count(submission_id) as 'subs' from submissions
                group by submission_date, hacker_id
            ) as t2
            group by t2.submission_date
        )as m
        on (c.submission_date = m.submission_date)
        where c.subs = m.maxday
    ) as main
    left join hackers h on (main.id = h.hacker_id)


    select c.submission_date, count( distinct c.hacker_id) as hackers, min(c.hacker_id) as 'id'
    from
    (
        select submission_date, hacker_id , count(submission_id) as 'subs' from submissions
        group by submission_date, hacker_id
    ) as c
    group by c.submission_date
    join 
    (
        select t2.submission_date , max(t2.subs) as 'maxday'
        from (        
            select submission_date, hacker_id , count(submission_id) as 'subs' from submissions
            group by submission_date, hacker_id
        ) as t2
        group by t2.submission_date
    )as m
    on (c.submission_date = m.submission_date)
where c.subs = m.maxday



CREATE TEMPORARY TABLE IF NOT EXISTS menagerie.users(
    id int not null default 0,
    user_action varchar(10),
    action_date date 
)
SELECT t1.* FROM (
    VALUES 
    ROW (1,'start', CAST('01-01-20' AS date)), 
    ROW (1,'cancel', CAST('01-02-20' AS date)), 
    ROW (2,'start', CAST('01-03-20' AS date)), 
    ROW (2,'publish', CAST('01-04-20' AS date)), 
    ROW (3,'start', CAST('01-05-20' AS date)), 
    ROW (3,'cancel', CAST('01-06-20' AS date)), 
    ROW (1,'start', CAST('01-07-20' AS date)), 
    ROW (1,'publish', CAST('01-08-20' AS date))
) as t1(id, user_action, action_date);

SHOW CREATE TABLE users;

with t1 AS 
    (
    SELECT id, 
        sum(CASE WHEN action = 'start' THEN 1 ELSE 0 END) AS starts, 
        sum(CASE WHEN action = 'cancel' THEN 1 ELSE 0 END) AS cancels, 
        sum(CASE WHEN action = 'publish' THEN 1 ELSE 0 END) AS publishes
    FROM users
        GROUP BY 1
        ORDER BY 1
    )
SELECT 
    id, 
    1.0*publishes/starts AS publish_rate, 
    1.0*cancels/starts AS cancel_rate
FROM t1



WITH users (user_id, action, date) 
AS (
    VALUES 
    ROW (1,'start', CAST('01-01-20' AS date)), 
    ROW (1,'cancel', CAST('01-02-20' AS date)), 
    ROW (2,'start', CAST('01-03-20' AS date)), 
    ROW (2,'publish', CAST('01-04-20' AS date)), 
    ROW (3,'start', CAST('01-05-20' AS date)), 
    ROW (3,'cancel', CAST('01-06-20' AS date)), 
    ROW (1,'start', CAST('01-07-20' AS date)), 
    ROW (1,'publish', CAST('01-08-20' AS date))),
t1 AS 
    (
    SELECT user_id, 
        sum(CASE WHEN action = 'start' THEN 1 ELSE 0 END) AS starts, 
        sum(CASE WHEN action = 'cancel' THEN 1 ELSE 0 END) AS cancels, 
        sum(CASE WHEN action = 'publish' THEN 1 ELSE 0 END) AS publishes
    FROM users
        GROUP BY 1
        ORDER BY 1
    )
SELECT 
    user_id, 
    1.0*publishes/starts AS publish_rate, 
    1.0*cancels/starts AS cancel_rate
FROM t1



-- From the following table of transactions between two users, 
-- write a query to return the change in net worth for each user, 
-- ordered by decreasing net change

CREATE TABLE transactions (
    sender int not null default 99,
    receiver int not null default 99,
    amount float not null default 0.0,
    trans_date date)
    SELECT * FROM (
        VALUES
        ROW (5, 2, 10, STR_TO_DATE('2-12-20','%m-%d-%Y')),
        ROW (1, 3, 15, STR_TO_DATE('2-13-20' ,'%m-%d-%Y')), 
        ROW (2, 1, 20, STR_TO_DATE('2-13-20' ,'%m-%d-%Y')), 
        ROW (2, 3, 25, STR_TO_DATE('2-14-20' ,'%m-%d-%Y')), 
        ROW (3, 1, 20, STR_TO_DATE('2-15-20' ,'%m-%d-%Y')), 
        ROW (3, 2, 15, STR_TO_DATE('2-15-20' ,'%m-%d-%Y')), 
        ROW (1, 4, 5, STR_TO_DATE('2-16-20' ,'%m-%d-%Y')))
        as t(sender, receiver, amount, trans_date);


with    debits AS (SELECT sender, sum(amount) AS debited FROM transactions GROUP BY sender ),
        credits AS (SELECT receiver, sum(amount) AS credited FROM transactions GROUP BY receiver )
SELECT 
    coalesce(sender, receiver) AS user, 
    coalesce(credited, 0) - coalesce(debited, 0) AS net_change 
FROM debits d
    left outer JOIN credits c ON d.sender = c.receiver
union 
    SELECT 
    coalesce(sender, receiver) AS user, 
    coalesce(credited, 0) - coalesce(debited, 0) AS net_change 
FROM debits d
    right outer JOIN credits c ON d.sender = c.receiver
ORDER BY 2 DESC


-- most frequent Item

WITH items (date, item) 
AS (
    VALUES 
    ROW (STR_TO_DATE('01-01-20' , '%m-%d-%Y'),'apple'), 
    ROW (STR_TO_DATE('01-01-20' , '%m-%d-%Y'),'apple'), 
    ROW (STR_TO_DATE('01-01-20' , '%m-%d-%Y'),'pear'), 
    ROW (STR_TO_DATE('01-01-20' , '%m-%d-%Y'),'pear'), 
    ROW (STR_TO_DATE('01-02-20' , '%m-%d-%Y'),'pear'), 
    ROW (STR_TO_DATE('01-02-20' , '%m-%d-%Y'),'pear'), 
    ROW (STR_TO_DATE('01-02-20' , '%m-%d-%Y'),'pear'), 
    ROW (STR_TO_DATE('01-02-20' , '%m-%d-%Y'),'orange')
    ),
-- add an item count column to existing table, grouping by date and item columns
t1 AS (
SELECT date, item, count(*) AS item_count
FROM items
GROUP BY 1, 2
ORDER BY 1),
-- add a rank column in descending order, partitioning by date
t2 AS (
SELECT *, rank() OVER (PARTITION by date ORDER BY item_count DESC) AS date_rank
FROM t1)
-- return all dates and items where rank = 1
SELECT date, item
FROM t2
WHERE date_rank = 1


SELECT *, 
    row_number() OVER user_window AS date_row,
    rank() OVER user_window AS date_rank
FROM users
WINDOW  user_window AS (PARTITION by id ORDER BY action_date DESC);



create TEMPORARY table likes (
    user_id int not null default 99, 
    page_likes char(1))
select * from (
    values 
    row (1, 'A'), 
    row (1, 'B'), 
    row (1, 'C'),
    row (2, 'A'),
    row (3, 'B'),
    row (3, 'C'),
    row (4, 'B')) as t(user_id, page_likes)


with t1 AS (
SELECT l.user_id, l.page_likes, f.friend
FROM likes l
JOIN friends f
ON l.user_id = f.user_id ),
-- left join likes on this, requiring user = friend and user likes = friend likes 
t2 AS (
SELECT t1.user_id, t1.page_likes, t1.friend, l.page_likes AS friend_likes
FROM t1
LEFT JOIN likes l
ON t1.friend = l.user_id
AND t1.page_likes = l.page_likes )
-- if a friend pair doesn’t share a common page like, friend likes column will be null - pull out these entries 
SELECT DISTINCT friend AS user_id, page_likes AS recommended_page
FROM t2
WHERE friend_likes IS NULL
ORDER BY 1 ASC;