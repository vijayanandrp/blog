import java.util.Locale
import spark.implicits._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.internal.SQLConf
import org.apache.spark.sql.types.{ArrayType, StringType}
import org.apache.spark.sql.{Column, DataFrame}
import org.apache.spark.sql.functions.countDistinct
import org.apache.spark.sql.types._

def CompareDataframe(left_df: DataFrame, right_df: DataFrame, pk_columns: Seq[String] = null, select_columns: Seq[String]  = null, limit: Int = 100): DataFrame = {

    // Record types
    val insertRecord = "Right"
    val deleteRecord = "Left"
    val changeRecord = "Change"
    val nochangeRecord = "Match"
    val diffcolumnName = "DiffType"

    // Left and Right column name
    val leftColumn = "left_"
    val rightColumn = "right_"
    val leftDF = left_df
    val rightDF = right_df
    val leftColumns = leftDF.columns.toSeq
    val rightColumns =  rightDF.columns.toSeq

    // SELECT 
    val selectColumns = if (select_columns == null) { 
      leftColumns.intersect(rightColumns)
    }  else select_columns
  

    // PRIMARY KEY COLUMNS
    val pkColumns = if (pk_columns == null) { 
      selectColumns.toSeq
    } else pk_columns

    // FINAL COLUMNS
    val selectColumnsList = if (pk_columns != null || select_columns != null){
      pkColumns.toSeq.union(selectColumns.toSeq).map(name => col(name))
    } else selectColumns.map(name => col(name))

    val left = leftDF.select(selectColumnsList:_*)
    val right = rightDF.select(selectColumnsList:_*)

    def columnName(columnName: String): String =
    if (SQLConf.get.caseSensitiveAnalysis) columnName else columnName.toLowerCase(Locale.ROOT)


    def distinctStringNameFor(existing: Seq[String]): String = {
    "_" * (existing.map(_.length).reduceOption(_ max _).getOrElse(0) + 1)
    }

    val pkColumnsCs = pkColumns.map(columnName).toSet
    val otherColumns = left.columns.filter(col => !pkColumnsCs.contains(columnName(col)))

    val existsColumnName = distinctStringNameFor(left.columns)
    val l = left.withColumn(existsColumnName, lit(1))
    val r = right.withColumn(existsColumnName, lit(1))
    val joinCondition = pkColumns.map(c => l(c) <=> r(c)).reduce(_ && _)
    val unChanged = otherColumns.map(c => l(c) <=> r(c)).reduceOption(_ && _)
    val changeCondition = not(unChanged.getOrElse(lit(true)))

    // DIff Condition
    val diffCondition = when(l(existsColumnName).isNull, lit(insertRecord)).
    when(r(existsColumnName).isNull, lit(deleteRecord)).
    when(changeCondition, lit(changeRecord)).
    otherwise(lit(nochangeRecord)).
    as(diffcolumnName)

    // Find DIff Columns
    val diffColumns =
    pkColumns.map(c => coalesce(l(c), r(c)).as(c)) ++ otherColumns.flatMap(c =>
    Seq(
        left(c).as(s"$leftColumn$c"),
        right(c).as(s"$rightColumn$c")
    )).toList


    val optionschangeColumn: Option[String] = None

    val changeColumn =
    optionschangeColumn.map(changeColumn =>
    when(l(existsColumnName).isNull || r(existsColumnName).isNull, lit(null)).
        otherwise(
        Some(otherColumns.toSeq).filter(_.nonEmpty).map(columns =>
            concat(
            columns.map(c =>
                when(l(c) <=> r(c), array()).otherwise(array(lit(c)))
            ): _*
            )
        ).getOrElse(
            array().cast(ArrayType(StringType, containsNull = false))
        )
        ).as(changeColumn)
    ).map(Seq(_)).getOrElse(Seq.empty[Column])

    val left_count =  leftDF.count()
    val right_count = rightDF.count() 

    Console.out.println( "Common Columns  - " + selectColumnsList.toList )
    Console.out.println( "Left Dataframe Count    - " + left_count)
    Console.out.println( "Right Dataframe Count    - " + right_count)

    if (left_count == right_count) {
    Console.out.println( " Both Left and Right dataframe count is matching. ")
    } else if ( left_count > right_count) {
    Console.out.println( " Left is having more count than right dataframe. Difference = " + (left_count - right_count))
    } else if ( left_count < right_count) {
    Console.out.println( " Right is having more count than left dataframe. Difference = " + (right_count - left_count))
    }

    val diffDF = l.join(r, joinCondition, "fullouter").select((diffCondition +: changeColumn) ++ diffColumns: _*)

    diffDF.groupBy(diffcolumnName).count().show(25, false)
    
  
    diffDF.orderBy(diffcolumnName).limit(limit)
}

val columns=Array("id", "first", "last", "year")
val df1 = spark.sparkContext.parallelize(Seq(
  (1, "John", "Doe", 1986),
  (2, "Ive", "Fish", 1990),
  (4, "John", "Wayne", 1995),
  (55, "Tom", "Cruise", 1978),
  (96, "Angelina", "Julie", 1985)
)).toDF(columns: _*)

val df2 = spark.sparkContext.parallelize(Seq(
  (1, "John", "Doe", 1986),
  (2, "IveNew", "Fish", 1990),
  (3, "San", "Simon", 1974),
  (55, "Tom", "Cruise", 1978),
  (96, "Angelina", "Joolie", 1987)
)).toDF(columns: _*)

val df = CompareDataframe(df1, df2,  Seq("id"), Seq("first", "last", "year"), 100)
df.show(25, false)
