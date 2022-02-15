"""
Find the total quantity previous year for a given dataset

season, geo, product, qty
2020SU, asia, shoes, 50
2020SU, asia, dresses, 80
2020SU, asia, dresses, 40
2020FA, asia, socks, 120
2021FA, asia, shoes, 90
2021SU, asia, dresses, 180
2021SU, asia, dresses, 10
2022SU, asia, dresses, 280
2022FA, asia, socks, 210
2020SU, europe, dresses, 60
2021SU, europe, dresses, 100
2022SU, europe, dresses, 280
2022FA, europe, socks, 210
2021SU, global, dresses, NULL
2022SU, global, dresses, NULL

Output:
season, geo, product, qty, qty_previous_year
2020SU, asia, dresses, 120, NULL
2021SU, asia, dresses, 190, 120
2022SU, asia, dresses, 280, 190
"""
import psycopg2
from psycopg2.extras import execute_values
import pandas
import warnings

warnings.filterwarnings('ignore')

# Connect to the postgresSQL server
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="N0P4ssw0rd!@#$",
    options="-c search_path=temp")
cur = conn.cursor()

table_name = "orders"
drop_table = f"""drop table if exists {table_name};"""
create_table = f""" create table if not exists {table_name} (
                        season varchar, 
                        geo varchar,
                        product varchar, 
                        qty integer
                    ); """
insert_table = f"""insert into {table_name} values %s"""
select_table = f"""select * from {table_name}"""
cur.execute(drop_table)
conn.commit()
cur.execute(create_table)
conn.commit()

data = """
2020SU, asia, shoes, 50
2020SU, asia, dresses, 80
2020SU, asia, dresses, 40
2020FA, asia, socks, 120
2021FA, asia, shoes, 90
2021SU, asia, dresses, 180
2021SU, asia, dresses, 10
2022SU, asia, dresses, 280
2022FA, asia, socks, 210
2020SU, europe, dresses, 60
2021SU, europe, dresses, 100
2022SU, europe, dresses, 280
2022FA, europe, socks, 210
2021SU, global, dresses, NULL
2022SU, global, dresses, NULL
""".replace("NULL", "0")

data = [tuple([_.strip() for _ in x.split(",")]) for x in data.split("\n") if x]
# print(data)

execute_values(cur, insert_table, data)
conn.commit()


def run_query(_query, option=1):
    if option == 0:
        cur.execute(_query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    else:
        df = pandas.read_sql_query(_query, con=conn)
        print(df.to_string(index=False))


result_query = f"""
select * 
, lag(qty) over (partition by geo, product order by season) as previous_year_qty
from (
select season, geo, product, sum(qty::int) as qty
from {table_name}
group by season, geo, product
order by season, geo, product, qty asc
) t
"""

run_query(result_query, option=1)
