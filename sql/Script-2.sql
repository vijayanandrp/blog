drop schema if exists temp cascade;

create schema if not exists temp;

set schema 'temp';

drop table if exists team;

truncate table team;

create table team (
	country VARCHAR(15) unique not null
);

insert into team values
('India'),
('Pakistan'),
('Srilanka'),
('Australia');



select a.country || ' vs ' ||  b.country fixture, 
current_timestamp 
from team a
cross join team b
where a.country < b.country
order by fixture asc

select a.country || ' vs ' ||  b.country fixture
from team a, team b
where a.country < b.country
order by fixture asc


select a.country || ' vs ' ||  b.country fixture
from team a
cross join  team b
where a.country <> b.country
order by fixture asc


select a.country || ' vs ' ||  b.country fixture
from team a, team b
where a.country <> b.country
order by fixture asc
