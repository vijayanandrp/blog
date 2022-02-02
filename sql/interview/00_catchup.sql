-- USING POSTGRES 

create schema if not exists temp;
set schema 'temp';


--Contents:
--1) Setup
--2) Selects and Counts
--3) Limit, Offset and Order By
--4) Joins
--5) Intersect, Union and Except
--6) Aliasing
--7) Aggregating Data
--8) Modifying Selected Values
--9) Where Clauses


--1) Setup

-- users whose information the company has
create table users (
 id serial primary key,
 first_name varchar (50),
 location varchar (50),
 created_at TIMESTAMP
);
-- users who are on the company mailing list
create table mailing_lists (
 id serial primary key,
 first_name varchar (50),
 email varchar (50),
 created_at TIMESTAMP
);
-- products the company sells
create table products (
 id serial primary key,
 name varchar(50),
 manufacturing_cost int,
 data jsonb,
 created_at TIMESTAMP
)
-- sales transactions of products by users
create table sales (
 id serial primary key,
 user_id int,
 product_id int,
 sale_price int,
 created_at TIMESTAMP 
);

alter table sales drop user_id;
alter table sales add user_id int;

insert into users (first_name, location, created_at)
values
 ('Liam', 'Toronto', '2010-01-01'),
 ('Ava', 'New York', '2011-01-01'),
 ('Emma', 'London', '2012-01-01'),
 ('Noah', 'Singapore', '2012-01-01'),
 ('William', 'Tokyo', '2014-01-01'),
 ('Oliver', 'Beijing', '2015-01-01'),
 ('Olivia', 'Moscow', '2014-01-01'),
 ('Mia', 'Toronto', '2015-01-01');

insert into mailing_lists (first_name, email, created_at)
values
 ('Liam', 'liam@fake.com', '2010-01-01'),
 ('Ava', 'ava@fake.com', '2011-01-01');

insert into products (name, manufacturing_cost, data, created_at)
values 
 ('laptop', 500, '{"in_stock":1}', '2010-01-01'),
 ('smart phone', 200, '{"in_stock":10}', '2010-01-01'),
 ('TV', 1000, '{}', '2010-01-01');

truncate table sales;
insert into sales (user_id, product_id, sale_price, created_at)
values
 (1, 1, 900, '2015-01-01'),
 (1, 2, 450, '2016-01-01'),
 (1, 3, 450, '2016-01-01'),
 (1, 3, 2500, '2017-01-01'),
 (2, 1, 800, '2017-01-01'),
 (2, 2, 600, '2017-01-01'),
 (3, 3, 2500, '2018-01-01'),
 (4, 3, 2400, '2018-01-01'),
 (null, 3, 2500, '2018-01-01'),
 (4, 3, 4000, '2018-01-01');

 

select * from sales;

select sale_price, 
rank() over (order by sale_price) as rank_func,
dense_rank() over (order by sale_price) as dense_rank_func
from sales;

select first_name from users
except 
select first_name from mailing_lists;



--02) Selects and Counts

select * from sales;

select first_name, location from users;

select distinct user_id from sales;

select count(*) from products;

select count(*) from (
  select * from products
  left join sales on sales.product_id = products.id
) subquery;

--03) Limit, Offset and Order By

select * from sales limit 3;

select 
  * 
from sales 
order by user_id asc -- desc
limit 3;

select * from sales 
order by user_id asc
limit 3 offset 0;

select * from sales 
order by user_id asc
limit 3 offset 3;


--04) Joins

select 
  * 
from users 
left join sales on sales.user_id = users.id;

select 
  * 
from users 
right join sales on sales.user_id = users.id;

select 
  * 
from users
inner join sales on sales.user_id = users.id;

select 
 * 
from users
full outer join sales on sales.user_id = users.id;


--05) Intersect, Union and Except

--Intersect
--Not really a join but it can be used like one. It has the benefit of being able to match on null values, something inner join cannot do.

select 
  first_name
from users
intersect
select 
  first_name
from mailing_lists;

--Union
--Allows you to return data from different columns, in the same column. 

-- We can also stack 2 columns from the same table. Here we have user locations and product names.
-- will remove duplicates automatically (its a set union)
select first_name from users 
union
select location from users;

select location from users
union
select name from products;

-- Use union all if you don’t want duplicates removed automatically.

select name from products
union all
select name from products

--Except
--We can exclude rows that exist in 2 tables, while returning the others. Return all names except those in both users and the mailing_lists.
select 
  first_name
from users
except
select 
  first_name
from mailing_lists;

--Aliasing
select 
  first_name as name,
  location as city
from users;

select 
  u.first_name,
  u.location
from users as u;

--Aggregating Data
--Grouping and aggregating data is a pretty powerful feature. Postgres provides the standard functions like: sum(), avg(), min(), max() and count().

select 
  product_id, 
  sum(sale_price),
  avg(sale_price),
  min(sale_price),
  max(sale_price),
  count(id)
from sales group by product_id;


select 
  products.name, 
  sum(sale_price),
  avg(sale_price),
  min(sale_price),
  max(sale_price),
  count(sales.id)
from sales
left join products on products.id = sales.product_id
group by products.name;


select 
  products.name, 
  sum(sale_price),
  avg(sale_price),
  min(sale_price),
  max(sale_price),
  count(sales.id)
from sales
left join products on products.id = sales.product_id
group by products.name
having count(sales.id) > 2;

--String_agg
--Can also use _agg functions (like string_agg) in combination with group by to build a comma delimited string of people who bought each product.

select 
 products.name,
 string_agg(users.first_name, ‘, ‘)
from products
left join sales on sales.product_id = products.id
left join users on users.id = sales.user_id
group by products.name;


--08) Modifying Selected Values
--Casting means converting the type of data in a column. Not all data can be converted to all datatypes. For instance, trying to cast a string to an integer would throw an error.
select 
  name, 
  manufacturing_cost / 3 cost_int,
  manufacturing_cost::decimal / 3 as cost2_dec,
  '2020–01–01'::text,
  '2020–01–01'::date
from products;

select 
  name, 
  round(manufacturing_cost::decimal / 3, 2 )
from products;
--
--Case
--Case allows conditionally applying logic or returning a different values based on a cell’s value. It’s SQL’s equivalent of if/else. Here we return the value 100 for cells where user_id is null.

select 
  id,
  case
    when user_id is null then 100
    else user_id
  end
from sales;

--Coalesce
--Coalesce allows returning the value from a different column if the first column’s value is null.
--Useful is data is really sparse or spread across multiple columns.

select 
  id,
  coalesce(user_id, product_id)
from sales;

--Concat
--Concat simply concatenates strings. Here we concatenate names and locations.
select 
 concat(first_name, ‘ ‘, location)
from users;

--Upper and lower
--Changes the case of a string.
--If this needs to be done somewhere in your data processing pipeline, doing it at the SQL level is significantly faster than at the python/app level.
select 
  upper(first_name),
  lower(first_name)
from users;

--09) Where Clauses
The big section.
Operators
We can use all the equality operators you’d expect in a where clause: =, <>, !=, <, <=, >=, > .
Find all records where the name is exactly “Liam”.

select * from users where first_name = 'Liam'

Find all records where the name is not “Liam”.
select * from users where first_name != 'Liam'

Find all records where id is greater or equal to 5.
select * from users where id >= 5

And, Or, Not
Chain multiple where clauses together with and, or and not. But notice we only write the where word once.
Select all records where the name is exactly “Liam” or “Olivia”.
select * from users where first_name = 'Liam' or first_name = 'Olivia';

Select all records where the name is exactly “Liam” AND the id is 5. This returns none because Liam’s id is not 5.
select * from users where first_name = 'Liam' and id = 5;

Select all records where the name is “Liam” AND the id is NOT 5. This returns Liam now.
select * from users where first_name = 'Liam' and not id = 5;

In
Rather than chaining clauses with or, or, or… you can find records where a value exists in a given array.
select * from users where first_name in ('Liam', 'Olivia');

Null
We can also load records where a value is (or is not) null.
select * from sales where user_id is null;
select * from sales where user_id is not null;


Fuzzy matching
Sometimes we want to find values that roughly match a query. For this, we can search on partial strings or ignore capitalization.
Load any records with the characters “ia” in the name.
select * from users where first_name like '%ia%';

Load records with the characters “IA” in the name. This returns nothing because no names have capitalized “IA” in them.
select * from users where first_name like '%IA%';

So let’s do a search ignoring cases.
select * from users where first_name ilike ‘%IA%’;

select 
  first_name 
from (
  select * from users where id > 5
) subquery;


with cte as (
  select * from users where id > 5
)
select 
  first_name
from cte

select first_name from users
intersect
select first_name from mailing_lists;


select 
 first_name as joined_user,
 lead(first_name) over (order by created_at) as next_joined_user
from users;

select 
 first_name as joined_user,
 lag(first_name) over (order by created_at) as prev_joined_user
from users;


CREATE DATABASE testDb 
WITH TEMPLATE postgres;