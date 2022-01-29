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
	
select * from cust_order co limit 10;

select * from order_line ol limit 10;

select count(distinct order_id) as num_orders, count(1) as total_records from cust_order co limit 10;

select count(distinct order_id) as num_orders, count(1) as total_records from order_line co limit 10;


select 'inner' as join_type, count(1) as total_records from cust_order co inner join order_line ol on ol.order_id = co.order_id 
union all
select 'left' as join_type, count(1) as total_records from cust_order co left join order_line ol on ol.order_id = co.order_id 
union all
select 'right' as join_type, count(1) as total_records from cust_order co right join order_line ol on ol.order_id = co.order_id 



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

	
/*
  ISSUE WITH QUERY 
  ===============
  	The LAG function will look at rows that are 7 rows earlier than the current row. Ideally, this means that it’s 7 days in the past.

	However, the order_date values come from the cust_order table, and there is no guarantee that there will be an order every day.

    LAG Function won't identify the missing days in past.
*/
	
	-- Calendar table 
create table calendar_days (
  calendar_date DATE,
  calendar_year INT,
  calendar_month INT,
  calendar_day INT,
  calendar_dayname VARCHAR(20)
);



create or replace procedure filldates(dateStart date, dateEnd date)
language plpgsql    
as $$
begin
  while dateStart <= dateEnd loop
  	truncate table calendar_days;
    insert into calendar_days 
    (calendar_date, calendar_year, calendar_month, calendar_day, calendar_dayname)
    values (
    dateStart, 
    to_char(dateStart, 'YYYY')::int, 
    to_char(dateStart, 'MM')::int,  
    to_char(dateStart, 'DD')::int,
    to_char(dateStart, 'Day')::varchar);
   dateStart := to_char(dateStart + '1 day'::interval, 'YYYY-MM-DD')::date;
  end loop;
 commit;
end;$$


truncate table calendar_days;

call filldates('2018-01-01', current_date);

select * from calendar_days;

/*
 UPDATED QUERY
 */
	
select
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname,
	count(distinct sub.order_id) as num_orders ,
	sum(sub.price) as total_price,
	count(sub.book_id) as num_books,
	sum(count(sub.book_id)) over (
		partition by c.calendar_year, c.calendar_month 
		order by c.calendar_date 
		) as running_total_num_books,
	lag(count(sub.book_id), 7) over (
		order by c.calendar_date
		) as prev_books
from calendar_days c
left join 
	(
	select
		to_char(co.order_date, 'YYYY-MM') as order_month,
		to_char(co.order_date, 'YYYY-MM-DD')::date as order_day,
		co.order_id ,
		ol.price,
		ol.book_id
	from
		cust_order co
	inner join order_line ol on
		co.order_id = ol.order_id 
) sub on sub.order_day  = c.calendar_date 
group by
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname
having count(distinct sub.order_id) > 0
order by
	c.calendar_date asc

/*
 Analyse and Improve Performance
 ===============================
 We can run an Explain Plan on this query and see what it shows.
 Create indexes
*/
	
CREATE INDEX idx_calendar_date ON calendar_days(calendar_date);
CREATE INDEX idx_ol_orderid ON order_line(order_id);


-- Optimize 1 to remove date format
select
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname,
	count(distinct sub.order_id) as num_orders ,
	sum(sub.price) as total_price,
	count(sub.book_id) as num_books,
	sum(count(sub.book_id)) over (
		partition by c.calendar_year, c.calendar_month 
		order by c.calendar_date 
		) as running_total_num_books,
	lag(count(sub.book_id), 7) over (
		order by c.calendar_date
		) as prev_books
from calendar_days c
left join 
	(
	select
		co.order_date,
		co.order_id ,
		ol.price,
		ol.book_id
	from
		cust_order co
	inner join order_line ol on
		co.order_id = ol.order_id 
) sub on sub.order_date::date  = c.calendar_date 
group by
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname
having 
	count(distinct sub.order_id) > 0
order by
	c.calendar_date asc
	
-- Optimize 2 remove the sub query
select
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname,
	count(distinct co.order_id) as num_orders ,
	sum(ol.price) as total_price,
	count(ol.book_id) as num_books,
	sum(count(ol.book_id)) over (
		partition by c.calendar_year, c.calendar_month 
		order by c.calendar_date 
		) as running_total_num_books,
	lag(count(ol.book_id), 7) over (
		order by c.calendar_date
		) as prev_books
from calendar_days c
left join cust_order co on c.calendar_date = co.order_date::date
inner join order_line ol on co.order_id = ol.order_id 
group by
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname
order by
	c.calendar_date asc

	
-- Optimize 3 inner join to left join
select
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname,
	count(distinct co.order_id) as num_orders ,
	sum(ol.price) as total_price,
	count(ol.book_id) as num_books,
	sum(count(ol.book_id)) over (
		partition by c.calendar_year, c.calendar_month 
		order by c.calendar_date 
		) as running_total_num_books,
	lag(count(ol.book_id), 7) over (
		order by c.calendar_date
		) as prev_books
from calendar_days c
left join cust_order co on c.calendar_date = co.order_date::date
left join order_line ol using(order_id)
where co.order_id is not null
group by
	c.calendar_date,
	c.calendar_year,
	c.calendar_month,
	c.calendar_dayname
order by
	c.calendar_date asc