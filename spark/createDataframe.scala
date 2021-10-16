import spark.implicits._
val sqlContext = new org.apache.spark.sql.SQLContext(sc)

val columns=Array("id", "first", "last", "year")
val df1=sc.parallelize(Seq(
  (1, "John", "Doe", 1986),
  (2, "Ive", "Fish", 1990),
  (4, "John", "Wayne", 1995)
)).toDF(columns: _*)

val df2=sc.parallelize(Seq(
  (1, "John", "Doe", 1986),
  (2, "IveNew", "Fish", 1990),
  (3, "San", "Simon", 1974)
)).toDF(columns: _*)
