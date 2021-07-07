import java.sql.Timestamp 
import org.apache.spark.sql.Row
import org.apache.spark.sql.types._

// 2017-07-14 02:40 UTC
val rdd = sc.parallelize(Row(new Timestamp(1500000000000L)) :: Nil)
val df = spark.createDataFrame(rdd, StructType(StructField("date", TimestampType) :: Nil))

df.select(df("date"), from_utc_timestamp(df("date"), "GMT+01:00") as "from_utc", to_utc_timestamp(df("date"), "GMT+01:00") as "to_utc").show(1, false)

// Date format printing is dependent on the timezone of the machine. 
// The following is in UTC
// +---------------------+---------------------+---------------------+             
// |date                 |from_utc             |to_utc               |
// +---------------------+---------------------+---------------------+
// |2017-07-14 02:40:00.0|2017-07-14 03:40:00.0|2017-07-14 01:40:00.0|
// +---------------------+---------------------+---------------------+

df.select(unix_timestamp(df("date")) as "date", unix_timestamp(from_utc_timestamp(df("date"), "GMT+01:00")) as "from_utc", unix_timestamp(to_utc_timestamp(df("date"),  "GMT+01:00")) as "to_utc").show(1, false)
// +----------+----------+----------+
// |date      |from_utc  |to_utc    |
// +----------+----------+----------+
// |1500000000|1500003600|1499996400|
// +----------+----------+----------+

df.select(unix_timestamp(df("date")) as "date", unix_timestamp(from_utc_timestamp(df("date"), "GMT+00:00")) as "from_utc", unix_timestamp(to_utc_timestamp(df("date"),  "GMT+00:00")) as "to_utc").show(1, false)

