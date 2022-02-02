-- USING POSTGRES 

create schema if not exists temp;

set schema 'temp';

drop table if exists salary;

create table employee (
	emp_name varchar not null,
	salary  int not null 
);



insert into employee  values
('John', 20),
('paul', 21),
('Roma', 19);


select sub.emp_name, sub.salary 
from (
select *, 
dense_rank() over (order by salary) as my_rank,
dense_rank() over (order by salary desc) as my_rank_desc
from employee ) sub
where my_rank = 1 or my_rank_desc = 1
order by salary 


select e.* from employee e
join (
select max(salary) as salary  from employee 
union 
select min(salary) as salary  from employee ) sub 
on sub.salary = e.salary 



select e.* from employee e
where salary in (
select max(salary) as salary  from employee 
union 
select min(salary) as salary  from employee ) 


