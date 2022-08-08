import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder().appName("Spark SQL basic example").getOrCreate()

// For implicit conversions like converting RDDs to DataFrames
import spark.implicits._


val sqlContext = new org.apache.spark.sql.SQLContext(sc)


val filePath = ""

val df = sqlContext.read.parquet(filePath)

val df = spark.read.parquet(filePath)

df.printSchema()

df.createOrReplaceTempView("PEOPLE")


val query =
    """
      SELECT * FROM PEOPLE
      """.stripMargin

val sqlDF = spark.sql(query)

sqlDF.show()
