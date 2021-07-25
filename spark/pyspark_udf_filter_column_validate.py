
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, BooleanType


spark = SparkSession.builder.master("Local[1]").appName("FilterExample").getOrCreate()

text = """
DR | 001 | 123456789 | 1234567890 | CA41 | 0
DR | 011 | 123456789 | 123456890 | CA451 | -1
DR | 111 | 12346789 | 1234567890 | CA451 | 01
DR | 999 | 123456789AA | 1234567890 | A451 | 0
DR | xxx | 123456789 | 1234567890 | CA451 | 0
DR | 00x | 123456789 | 123457890 | CA451 | -1
DR | 0x1 | 123456789 | 1234567890 | CA451 | 110

CP | 10111 | 123456789 | 1234567890 | CA451 | 011
CP | 0117Y | 123456789 | 1234567890 | CA451 | -1
CP | 1111T | 123456789 | 1234567890 | CA451 | 0
CP | 90999 | 123456789 | 1234567890 | CA451 | -1
CP | xxx | 123456789 | 1234567890 | CA451 | -1
CP | 00x | 123456789 | 123456890 | 451 | 0
CP | 0x1 | 123456789 | 1234567890 | CA451 | -1

HCP | V0111 | 12356789 | 12345W67890 | C451 | 0
HCP | A0117 | 123456789 | 12345890 | CA451 | -1
HCP | U1111 | 12345789 | 1234567890 | CA451 | 10
HCP | 9999999 | 123456789 | 1234567890 | CA451 | -1
HCP | xxx | 123456789 | 1234567890 | CA451 | -1
HCP | 0x1 | 1234567SS89 | 1234567890 | CA451 | 1

ADR | 0081 | 123456789 | 1234567890 | CT451 | 01
ADR | 0181 | 123456789 | 1234567890 | CA451 | -1
ADR | 1118 | 123456789 | 12347890 | C451 | 0
ADR | 9998 | 12345789 | 1234567890 | CA451 | 0
ADR | xxxggg | 123456789 | 1234567890 | CA451 | 0
ADR | 00gx | 123456789 | 1234567890 | CA451 | -1
ADR | 0x45671 | 123456789 | 1234567890 | C451 | 0

ADA | 10081 | 123456789 | 1234567890 | CA451 | 0
ADA | 01681 | 123456789 | 1234567890 | CA451 | -1
ADA | 11018 | 1234789 | 1234567890 | CA451 | 0
ADA | 99908 | 123456789 | 1234567890 | YA451 | 10
ADA | xxxggg | 123456789 | 1234567890 | CA451 | 0
ADA | 00gx | 123456789 | 1234567890 | CA451 | -1
ADA | 0x45671 | 123456789 | 1234567890 | ZA451 | 0

 """

data = [tuple(t.split(" | ")) for t in text.split("\n")  if t.strip()]

columns = ["code_type", "code_value", "nit", "ipn", "id_tn", "neg_rate"]
df = spark.createDataFrame(data=data, schema=columns)

df.printSchema()
df.show(truncate=False)

def validate_code_type(code, value):
    value = str(value).strip()
    if code == "DR":
        if not (len(value) == 3 and value.isdigit()):
            return False
        return True
    elif code == "CP":
        if not len(value) == 5:
            return False
        if value.isdigit() or (value[:4].isdigit() and value[4].isalpha()):
            return True
        else:
            return False
    elif code == "HCP":
        if not (len(value) == 5 and value[:1].isalpha() and value[1:].isdigit()):
            return False
        return True
    elif code == "ADR":
        if not (len(value) == 4 and value.isdigit()):
            return False
        return True
    elif code == "ADA":
        if not (len(value) == 5 and value.isdigit()):
            return False
        return True


def validate_nit(value):
    value = str(value).strip()
    if not (len(value) == 9 and value.isdigit()):
        return False
    return True


def validate_ipn(value):
    value = str(value).strip()
    if not (len(value) == 10 and value.isdigit()):
        return False
    return True

def validate_id_tn(value):
    value = str(value).strip()
    if not (len(value) == 5 and value[:2].isalpha() and value[2:5].isdigit()):
        return False
    return True


def validate_neg_rate(value):
    if int(value) <= 0:
        return True
    else:
        return False

def validate_neg_rate(value):
    if int(value) <= 0:
        return True
    else:
        return False

def validate_is_accepted(is_code_type, is_nit, is_ipn, is_id_tn, is_neg_rate):
    if is_code_type and is_nit and is_ipn and is_id_tn and is_neg_rate:
        return True
    else:
        return False

udf_validate_code_type = udf(lambda code, value: validate_code_type(code, value), BooleanType())
udf_validate_nit = udf(lambda value: validate_nit(value), BooleanType())
udf_validate_ipn = udf(lambda value: validate_ipn(value), BooleanType())
udf_validate_id_tn = udf(lambda value: validate_id_tn(value), BooleanType())
udf_neg_rate = udf(lambda value: validate_neg_rate(value), BooleanType())
udf_is_accepted = udf(lambda is_code_type, is_nit, is_ipn, is_id_tn, is_neg_rate:
    validate_is_accepted(is_code_type, is_nit, is_ipn, is_id_tn, is_neg_rate),
    BooleanType())


df = df.withColumn("is_code_type", udf_validate_code_type(col("code_type"), col("code_value")))
df = df.withColumn("is_nit", udf_validate_nit(col("nit")))
df = df.withColumn("is_ipn", udf_validate_ipn(col("ipn")))
df = df.withColumn("is_id_tn", udf_validate_id_tn(col("id_tn")))
df = df.withColumn("is_neg_rate", udf_neg_rate(col("neg_rate")))
df = df.withColumn("is_accepted", udf_is_accepted(col("is_code_type"),
                                               col("is_nit"),  col("is_ipn"),
                                               col("is_id_tn"), col("is_neg_rate")))

df.printSchema()
df.select(*["code_type", "code_value",  "is_code_type", "nit","is_nit",
 "ipn", "is_ipn", "id_tn", "is_id_tn",
 "neg_rate", "is_neg_rate", "is_accepted"]).show(80, truncate=False)



# ["code_type", "code_value", "nit", "ipn", "id_tn", "neg_rate",
# "is_code_type", "is_nit", "is_ipn", "is_id_tn", "is_neg_rate"]
