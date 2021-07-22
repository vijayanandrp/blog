from pyspark.sql.types import StructType,StructField, StringType, IntegerType

spark = SparkSession.builder.master("local[1]") \
                    .appName('SparkByExamples.com') \
                    .getOrCreate()

data = [
    ("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",1000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",7000),
    ("Jen","Mary","Brown","","F",-1),
    ("Kin","","Blue",None,"F",-1),
    (None, None, None,"","F",None),
    ("Michael",None,"","40288","M",1000),
    (None,"","Williams","42114","M",4000),
    ("Maria",None,"Jones","39192","F",7000)
  ]

columns = ["firstname", "middlename", "lastname", "id", "gender", "salary"]
df = spark.createDataFrame(data=data).toDF(*columns)
df.printSchema()
df.show(truncate=False)

schema = StructType([
    StructField("firstname",StringType(),False),
    StructField("middlename",StringType(),True),
    StructField("lastname",StringType(),True),
    StructField("id", StringType(), False),
    StructField("gender", StringType(), True),
    StructField("salary", IntegerType(), True)
  ])


def convert_epmty_to_null(df, columns):
    for _x in columns:
        df = df.withColumn(_x, when(col(_x) == '', None).otherwise(col(_x)))
    return df

def convert_null_to_epmty(df):
    return df.na.fill('')


def validate_dataframe_schema(df, schema):
    null_check_cols = []
    for _s in schema:
        _name = _s.name
        _datatype = _s.dataType
        _nullable = _s.nullable
        if not _nullable:
            null_check_cols.append(_name)
    df = convert_epmty_to_null(df, null_check_cols)
    df = df.na.drop(subset=null_check_cols)
    return df

df = convert_null_to_epmty(validate_dataframe_schema(df, schema))
df.show(truncate=False)


"""
spark.sql('SELECT * FROM DB.TBL LIMIT 100;')
"""










schema = StructType([
    StructField("firstname",StringType(),True),
    StructField("middlename",StringType(),True),
    StructField("lastname",StringType(),True),
    StructField("id", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("salary", IntegerType(), True)
  ])


df = spark.createDataFrame(data=data, schema=schema)
df.printSchema()
df.show(truncate=False)
