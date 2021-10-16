
### Missing columns finding 

```sql
create or replace table xxx1(i int, j int);
create or replace table xxx2(i int, k int);

-- Query from the original post
SELECT column_name
FROM information_schema.columns 
WHERE table_name = 'XXX1'
    AND column_name NOT IN
    (
        SELECT column_name
        FROM information_schema.columns 
        WHERE table_name = 'XXX2'
    );
-------------+
 COLUMN_NAME |
-------------+
 J           |
-------------+
```

```sql
with 
s1 as (
  select table_name, column_name 
  from information_schema.columns 
  where table_name = 'XXX1'), 
s2 as (
  select table_name, column_name 
  from information_schema.columns 
  where table_name = 'XXX2') 
select * from s1 full outer join s2 on s1.column_name = s2.column_name;
------------+-------------+------------+-------------+
 TABLE_NAME | COLUMN_NAME | TABLE_NAME | COLUMN_NAME |
------------+-------------+------------+-------------+
 XXX1       | I           | XXX2       | I           |
 XXX1       | J           | [NULL]     | [NULL]      |
 [NULL]     | [NULL]      | XXX2       | K           |
------------+-------------+------------+-------------+
```

### Missing records or diff records 

```sql
SELECT *  
FROM T1 AS T, T2 AS N 
WHERE T.ID       IS NOT DISTINCT FROM N.ID 
  AND T.TYPE     IS NOT DISTINCT FROM N.TYPE 
  AND T.MODEL_ID IS NOT DISTINCT FROM N.MODEL_ID 
  AND T.FREQ     IS NOT DISTINCT FROM N.FREQ;
```
 
 ```sql
SELECT * FROM t1
INTERSECT
SELECT * FROM T2;
```

 ```sql
Select * from ( 
Select pk_col, col1, col2...,coln from table1, ‘Old_table’ 
Union all 
Select pk_col, col1, col2...,coln from table2, 'New_table' 
) Temp order by pk_col;
```

```sql
Select Id_pk, col1, col2...,coln from table1 
MINUS
Select Id_pk, col1, col2...,coln from table2;
```

```sql
SELECT * FROM .dbo.Table1 A
LEFT JOIN dbo.Table2 S
ON A.ID =B.ID;
```


```sql
Select id_pk, col1, col2,col,… From table1 A
Where NOT EXISTS
( select 1 from table2 B
Where A.id_pk = B.id_pk
and A.col1 = B.col1
and A.col2 = B.col2
and…
);
```

 URL -https://stackoverflow.com/questions/46662816/snowflake-get-a-list-of-mismatching-columns-between-two-tables-sql
 
 URL - https://copycoding.com/d/how-to-compare-two-tables-in-sql-efficiently-quick-and-easy-method
 
