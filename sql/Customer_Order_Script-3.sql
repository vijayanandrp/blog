
/*
You are given following two tables,
Customer {cust_id, cust_name, ...<Other customer related details>}
Order {order_id, order_name, cust_id, ...<Other order related details>}
*/

-- Setup
drop schema if exists temp cascade;

create schema temp;

set schema 'temp';

create table customers (
	cust_id serial primary key,
	cust_name varchar(50) not null,
	gender varchar (10) not null
);

drop table orders;

create table orders (
	order_id int not null,
	order_name varchar (100),
	order_dt timestamp,
	order_price int,
	cust_id int not null,
	foreign key (cust_id) 
    references customers  (cust_id)
);

insert into customers (cust_name, gender)
values 
('Vijay', 'M'),
('Moni', 'F'),
('Kavi', 'M'),
('Adya', 'F'),
('Ras', 'M'),
('Liya', 'F');

select * from customers ;

explain analyze select distinct gender from customers c order by gender 

truncate table orders;

insert into orders ( order_id, order_name, cust_id, order_dt, order_price)
values 
(1, 'Laptop',1,'20220101',100),
(1, 'Headphones',1,'20220105',50),
(2, 'TV',2,'20200201',300),
(3, 'Cleaner',3,'20200101',400),
(3, 'PS',3,'20201221',600),
(4, 'Laptop',3,'20220101',1000),
(4, 'Headphones',3,'20220105',500),
(5, 'TV',2,'20200201',300);

select * from orders;

/*

Question 1: print only those customer who have at least one order.
You have to provide the output in following format.
cust_id, cust_name, [Total amount of orders]

*/

select c.*, t.total_orders 
from customers c
join (
select cust_id, count( distinct order_id) as total_orders 
from orders 
group by cust_id 
having count(distinct order_id) > 0
) t
on t.cust_id  = c.cust_id 

/*
Question 2: Find out all customers who haven't placed any order in the past six months.
*/
select c.* from customers c
where c.cust_id not in (
select distinct cust_id from orders
where order_dt > to_char(current_date - interval '6 months', 'YYYY-MM-DD')::date
) 

/*
Question 3: write a SQL query to find out customer's total purchasing payment in the past six months.
*/

select  c.*, o.total_payment  from customers c
join (
select cust_id, sum(order_price) as total_payment from orders 
where order_dt > to_char(current_date - interval '6 months', 'YYYY-MM-DD'):: date 
group by cust_id
) o
on o.cust_id = c.cust_id 

-- Extras

select to_char(current_date - interval '1 months', 'YYYY-MM-01'):: date;
select to_char(current_date - interval '6 months', 'YYYY-MM-DD'):: date;
select to_char(current_date - interval '30 days', 'YYYY-MM-DD'):: date;


/*
Question 4: write a SQL query to find out top 3 order price 
*/

select * 
from (
select *, 
dense_rank () over (order by order_price desc) as my_rank
from orders
) s
where my_rank <= 3


-- Example top 5 product sold in city 
select City, Orderid, total_quantity,
rank() OVER (PARTITION BY City ORDER BY total_quantity desc) as rank_quantity
 from table
 order by rank_quantity,city 
LIMIT 5;
