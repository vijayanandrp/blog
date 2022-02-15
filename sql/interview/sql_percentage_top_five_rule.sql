-- USING POSTGRES 
/*
 
 Problem Statement: 
 ==================
 For the 2022 academic year, students have appeared in the SSC exam and below is their result. 
You must calculate the percentage of results using the best of the five rule. 

i.e. you must take the top five grades for each student and calculate the percentage.
 
Id,English,Maths,Science,Geography,History,Sanskrit
 
1,85,99,92,84,84,99 
2,81,82,83,84,95,96 
3,75,55,75,75,55,75 
4,82,82,82,82,82,82 
5,83,99,45,88,76,89 


Result
======
id Engish Maths Science Geography History Sanscrit Percentage 
1 85 99 92 84 84 99 91.8000 
2 81 82 83 84 95 96 88.0000 
3 75 55 75 75 55 75 71.0000 
4 82 82 82 82 82 82 82.0000 
5 83 99 45 88 76 89 87.0000 


 */
create schema if not exists temp;

set schema 'temp';

create table marks (
	id int not null,
	english int,
	maths int,
	science int,
	geography int,
	history int,
	sanskrit int
);

insert into marks 
values 
	(1,85,99,92,84,84,99),
	(2,81,82,83,84,95,96),
	(3,75,55,75,75,55,75),
	(4,82,82,82,82,82,82),
	(5,83,99,45,88,76,89);

select * from marks;
	
	
select
*,
(((english + maths + science + geography + history + sanskrit) - 
(select min(col) from (values (english),(maths),(science),(geography),(history),(sanskrit)) as x(col))::numeric)
/ 5.0) as percentage
from marks

select
*,
(((english + maths + science + geography + history + sanskrit)  - 
least(english,maths,science,geography,history,sanskrit)) / 5.00) as percentage
from marks