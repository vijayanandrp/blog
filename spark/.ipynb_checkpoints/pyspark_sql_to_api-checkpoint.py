
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = SparkSession.builder.master("Local[1]").appName("FilterExample").getOrCreate()

text = """
DR | 011 | 123456789 | 1234567890 | CA41 | 0
DR | 011 | 123456789 | 123456890 | CA451 | -1
DR | 011 | 12346789 | 1234567890 | CA451 | 01
DR | 999 | 123456789AA | 1234567890 | A451 | 0
DR | xxx | 123456789 | 1234567890 | CA451 | 0
DR | 999 | 123456789 | 123457890 | CA451 | -1
DR | 999 | 123456789 | 1234567890 | CA451 | 110

CP | 10111 | 123456789 | 1234567890 | CA451 | 011
CP | 10111 | 123456789 | 1234567890 | CA451 | -1
CP | 10111 | 123456789 | 1234567890 | CA451 | 0
CP | 10111 | 123456789 | 1234567890 | CA451 | -1
CP | 10111 | 123456789 | 1234567890 | CA451 | -1
CP | 10111 | 123456789 | 123456890 | 451 | 0
CP | 10111 | 123456789 | 1234567890 | CA451 | -1

HCP | V0111 | 12356789 | 12345W67890 | C451 | 0
HCP | A0117 | 123456789 | 12345890 | CA451 | -1
HCP | U1111 | 12345789 | 1234567890 | CA451 | 10
HCP | 9999999 | 123456789 | 1234567890 | CA451 | -1
HCP | xxx | 123456789 | 1234567890 | CA451 | -1
HCP | 0x1 | 1234567SS89 | 1234567890 | CA451 | 1

ADR | 1118 | 123456789 | 1234567890 | CT451 | 01
ADR | 1118 | 123456789 | 1234567890 | CA451 | -1
ADR | 1118 | 123456789 | 12347890 | C451 | 0
ADR | 9998 | 12345789 | 1234567890 | CA451 | 0
ADR | 9998 | 123456789 | 1234567890 | CA451 | 0
ADR | 00gx | 123456789 | 1234567890 | CA451 | -1
ADR | 00gx | 123456789 | 1234567890 | C451 | 0

ADA | 10081 | 1234789 | 123567890 | CA451 | 0
ADA | 10081 | 123456789 | 123467890 | CA451 | -1
ADA | 10081 | 1234789 | 1234567890 | CA451 | 0
ADA | 99908 | 123456789 | 1234567890 | YA451 | 10
ADA | 99908 | 123456789 | 123467890 | CA451 | 0
ADA | 00gx | 123456789 | 12345670 | CA451 | -1
ADA | 00gx | 123456789 | 12367890 | ZA451 | 0

 """

data = [tuple(t.split(" | ")) for t in text.split("\n")  if t.strip()]

columns = ["code_type", "code_value", "neg_rate", "nit", "ipn", "id_tn"]
df = spark.createDataFrame(data=data, schema=columns)

df.groupBy("code_type", "code_value", "neg_rate").agg(concat_ws(",", collect_list(concat(coalesce(col("nit"), lit(None)), lit(':'), coalesce(col("ipn"), lit(None)), lit(':'), coalesce(col("id_tn"), lit(None))))).alias("prov_id")).withColumn("date_stamp", date_add(last_day(current_date()), 1)).select("date_stamp", "prov_id", "code_type", "code_value", "neg_rate").show(20, False)
