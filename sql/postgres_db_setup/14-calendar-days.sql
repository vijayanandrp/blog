set schema 'gravity_books';


create table calendar_days (
  calendar_date DATE,
  calendar_year INT,
  calendar_month INT,
  calendar_day INT,
  calendar_dayname VARCHAR(20)
);



create or replace procedure filldates(dateStart DATE, dateEnd DATE)
language plpgsql    
as $$
begin
  while dateStart <= dateEnd loop
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