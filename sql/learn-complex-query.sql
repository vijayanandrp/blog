/*
Complex SQL Query Example – Daily Order Analysis (Tried in Postgresql)
===========================================================================
 
 Source & Thanks - https://www.databasestar.com/complex-sql-query-example/
  
 Setup the database in postgres using the following scripts in order
 
 https://github.com/vijayanandrp/blog/tree/main/sql/postgres_db_setup
 
 */

set
schema 'gravity_books';

/*
* the order date
the number of orders for that date
the number of books ordered
the total price of the orders
the running total of books for the month
the number of books from the same day last week (e.g. how this Sunday compares to last Sunday)

 Start with a simple query to see the order date.
*/


select
	order_date
from
	cust_order co
order by
	order_date desc;

/*
Show Number of Orders Per Date
==============================
Whenever we need to see something like “the number of X per Y”, it usually means we need to use an aggregate function and group the results.
*/
-- Wrong Basically We need to change the query to show only the date and not the time.
select 
	order_date,
	count(*)
from
	cust_order co
group by
	order_date
order by
	order_date asc;
-- Right one
select
	to_char(order_date, 'YYYY-MM-DD') as order_day,
	count(order_id) as num_orders
from
	cust_order
group by
	to_char(order_date, 'YYYY-MM-DD')
order by
	order_day asc

/*
 Add Number of Books Ordered
 ===========================
 */
	
select
	*
from
	cust_order co
limit 10;

select
	*
from
	order_line ol
limit 10;

select
	to_char(co.order_date, 'YYYY-MM-DD') as order_day ,
	count(distinct co.order_id) as num_orders,
	count(distinct ol.book_id) as num_books
from
	cust_order co
inner join order_line ol 
on
	ol.order_id = co.order_id
group by
	to_char(co.order_date, 'YYYY-MM-DD')
order by
	order_day asc

/*
 Add Total Price of the Books
 ============================
 */
	select
	to_char(co.order_date, 'YYYY-MM-DD') as order_day ,
	count(distinct co.order_id) as num_orders,
	count(ol.book_id) as num_books,
	sum(ol.price) as total_price
from
	cust_order co
inner join order_line ol 
on
	ol.order_id = co.order_id
group by
	to_char(co.order_date, 'YYYY-MM-DD')
order by
	order_day asc

/*
 Add Running Total
 ==================
 */
	
select
	to_char(co.order_date, 'YYYY-MM') as order_month,
	to_char(co.order_date, 'YYYY-MM-DD') as order_day ,
	count(distinct co.order_id) as num_orders,
	count(ol.book_id) as num_books,
	sum(ol.price) as total_price,
	sum(count(ol.book_id)) over ( partition by to_char(co.order_date, 'YYYY-MM')
					order by to_char(co.order_date, 'YYYY-MM-DD')) as running_total_num_books
from
	cust_order co
inner join order_line ol on
	ol.order_id = co.order_id
group by
	to_char(co.order_date, 'YYYY-MM') ,
	to_char(co.order_date, 'YYYY-MM-DD')
order by
	order_day asc

/*
 Reformat Query
 ==================
 */

select
	order_month ,
	order_day,
	count(distinct order_id) as num_orders ,
	count(book_id) as num_books,
	sum(price) as total_price,
	sum(count(book_id)) over (partition by order_month order by order_day) as running_total_num_books
from
	(
	select
		to_char(co.order_date, 'YYYY-MM') as order_month,
		to_char(co.order_date, 'YYYY-MM-DD') as order_day,
		co.order_id ,
		ol.price,
		ol.book_id
	from
		cust_order co
	inner join order_line ol on
		co.order_id = ol.order_id 
) sub
group by
	order_month ,
	order_day
order by
	order_day asc

/*
Add Number from Last Week
=========================
LEAD lets you get data from rows further down (below) in the results, 
LAG lets you get data from rows further up (above) in the results.

As we’re ordering by order date in ascending order,
the earlier orders are further up the results, so we can use LAG.

We use LAG to get a value from an order date from one week ago, or seven days.

LAG is used as an analytic function, so we specify the OVER clause and the ORDER BY clause to define how the data is searched.
*/

select
	order_month ,
	order_day,
	count(distinct order_id) as num_orders ,
	sum(price) as total_price,
	count(book_id) as num_books,
	sum(count(book_id)) over (partition by order_month order by order_day) as running_total_num_books,
	lag(count(book_id), 7) over (order by order_day) as prev_books
from
	(
	select
		to_char(co.order_date, 'YYYY-MM') as order_month,
		to_char(co.order_date, 'YYYY-MM-DD') as order_day,
		co.order_id ,
		ol.price,
		ol.book_id
	from
		cust_order co
	inner join order_line ol on
		co.order_id = ol.order_id 
) sub
group by
	order_month ,
	order_day
order by
	order_day asc



