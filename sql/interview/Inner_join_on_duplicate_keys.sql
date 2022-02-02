-- USING POSTGRES 

create schema temp;

set schema 'temp';

CREATE TABLE t1 (
	c1 INT not NULL
);

CREATE TABLE d1 (
	c1 INT not NULL
);

insert into t1 values(1),(0),(0),(1),(0),(1);
insert into d1 values(0),(1),(0),(1),(0),(0);

select * from t1 as t1
inner join d1 as d1 
on t1.c1 = d1.c1 ;

/*
 Total Records 18 as output 


 How?
 
total value 1 in table t1 = 3
total value 1 in table d1 = 2
total value 1 in INNER JOIN = 3 * 2 = 6

total value 0 in table t1 = 3
total value 0 in table d1 = 4
total value 0 in INNER JOIN = 3 * 4 = 12

RESULT
======
c1	c1
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
1	1
1	1
1	1
1	1
1	1
1	1
*/