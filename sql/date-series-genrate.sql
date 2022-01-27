set schema 'temp';


select *, lead(s.day1) over(order by day1) as next_day from
(select to_char(to_date('2022-01-26', 'YYYY-MM-DD') + interval '15 days', 'YYYY-MM-DD')::date  day1) s
;

select to_char(to_date('2022-01-26', 'YYYY-MM-DD') + interval '15 days', 'YYYY-MM-DD')::date 

select to_char('2022-01-26'::date + interval '15 days', 'YYYY-MM-DD')::date 

select date::date from generate_series('2022-01-24'::date, '2022-07-26'::date, '15 days'::interval) date
/*
2022-01-26
2022-02-10
2022-02-25
2022-03-12
2022-03-27
2022-04-11
2022-04-26
2022-05-11
2022-05-26
2022-06-10
2022-06-25
2022-07-10
2022-07-25
*/