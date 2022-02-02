-- USING POSTGRES 

create schema if not exists temp;

set schema 'temp';

drop table if exists details;

create table details (
	student_id int not null,
	subject_id varchar not null,
	marks int not null 
);



insert into details values
(1, 's1', 60),(2, 's2', 90),(3, 's3', 70),
(1, 's1', 80),(2, 's2', 40),(3, 's3', 94),
(1, 's1', 73),(2, 's2', 84),(3, 's3', 52);

select * from details

select student_id 
from details 
where marks > 50
group by 
	student_id 
having count(subject_id)::int = (select count(distinct subject_id) from details )
order by 
	student_id asc


select distinct student_id 
from details 
where student_id  not in (select distinct student_id from details where marks < 50)