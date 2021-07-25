from datetime import datetime
import pytz
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType


def parse_utc_str(text):
    return text.replace("0 +00:00", "").strip()

def date_diff(start, end):
    tz_cst = pytz.timezone("US/Central")
    tz_gmt = pytz.timezone("UTC")
    dt_cst = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
    dt_gmt  = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
    dt_cst_start =  dt_cst.astimezone(tz_cst)
    dt_cst_end= dt_gmt.astimezone(tz_gmt)
    time_delta = dt_cst_end - dt_cst_start
    return  time_delta.total_seconds()


udf_parse_utc_str = udf(lambda z: parse_utc_str(z), StringType())
udf_date_diff = udf(lambda start,end: date_diff(start, end), StringType())

spark = SparkSession.builder.master("Local[1]").appName("TimeDiff").getOrCreate()

text = """
2002 | 2021-07-21 08:21:14.067 | 2021-07-21 13:12:45.2450000 +00:00
2003 | 2021-07-21 08:21:14.067 | 2021-07-21 13:12:45.2480000 +00:00
2004 | 2021-07-21 08:21:14.067 | 2021-07-21 13:12:46.6610000 +00:00
2005 | 2021-07-21 08:21:14.083 | 2021-07-21 13:12:47.2830000 +00:00
2007 | 2021-07-21 08:21:14.113 | 2021-07-21 13:12:43.4820000 +00:00
2008 | 2021-07-21 08:21:14.130 | 2021-07-21 13:12:47.2920000 +00:00
2009 | 2021-07-21 08:21:14.143 | 2021-07-21 13:12:47.2430000 +00:00
2010 | 2021-07-21 08:21:14.160 | 2021-07-21 13:12:46.6240000 +00:00
2011 | 2021-07-21 08:21:14.160 | 2021-07-21 13:12:47.2480000 +00:00
2012 | 2021-07-21 08:21:14.177 | 2021-07-21 13:12:47.1370000 +00:00
 """

data = [tuple(t.split(" | ")) for t in text.split("\n")  if t.strip()]
print(data)

columns = ["log_id", "date_cst", "date_gmt"]
df = spark.createDataFrame(data=data, schema=columns)
df.printSchema()
df.show(truncate=False)

df = df.withColumn("date_gmt", udf_parse_utc_str(col("date_gmt")))
df.show(truncate=False)

df = df.withColumn("date_diff(seconds)", udf_date_diff(col("date_gmt"), col("date_cst")))
df.show(truncate=False)

for t in data:
    tz_cst = pytz.timezone("US/Central")
    tz_gmt = pytz.timezone("UTC")
    dt_cst = datetime.strptime(t[1].strip(), "%Y-%m-%d %H:%M:%S.%f")
    dt_gmt  = datetime.strptime(t[2].replace("0 +00:00", "").strip(), "%Y-%m-%d %H:%M:%S.%f")
    dt_cst_start =  dt_cst.astimezone(tz_cst)
    dt_cst_end= dt_gmt.astimezone(tz_gmt)
    time_delta = dt_cst_end - dt_cst_start
    print(dt_cst_start, dt_cst_end, time_delta.total_seconds())
    # print(time_delta.total_seconds())
