import java.util.Locale
import spark.implicits._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.internal.SQLConf
import org.apache.spark.sql.types.{ArrayType, StringType}
import org.apache.spark.sql.{Column, DataFrame}
import org.apache.spark.sql.functions.countDistinct
import org.apache.spark.sql.types._


Console.out.println(Console.RED + " -*- STARTED Comparator Tool -*- " + Console.RESET)

val sqlContext = new org.apache.spark.sql.SQLContext(sc)

val oracleEtlPath = "XXXXXXXXXXXXXXXXXX"
val sdlEtlPath = "XXXXXXXXXXXXXXXX"


Console.out.println(Console.BLUE + "Oracel Etl - " + oracleEtlPath + Console.RESET)
Console.out.println(Console.BLUE + "SDL Etl    - " + sdlEtlPath + Console.RESET)


// Record types
val insertRecord = "Spark"
val deleteRecord = "Oracle"
val changeRecord = "Change"
val nochangeRecord = "NoChange"
val diffcolumnName = "DiffStatus"

// Left and Right column name
val leftColumn = "left_"
val rightColumn = "right_"



val leftDF = sqlContext.read.parquet(oracleEtlPath)
val rightDF = sqlContext.read.parquet(sdlEtlPath)

Console.out.println(Console.YELLOW + "Before LEFT Columns    - " + leftDF.columns.toSeq + Console.RESET)
Console.out.println(Console.CYAN + "Before RIGHT Columns    - " + rightDF.columns.toSeq + Console.RESET)

Console.out.println(Console.YELLOW + "Before LEFT Count    - " + leftDF.count() + Console.RESET)
Console.out.println(Console.CYAN + "Before RIGHT Count    - " + rightDF.count() + Console.RESET)

val leftColumns = leftDF.columns.toSeq
val rightColumns =  rightDF.columns.toSeq

val selectColumns = leftColumns.intersect(rightColumns)
val selectColumnsList = selectColumns.map(name => col(name))

// PRIMARY KEY COLUMNS
val pkColumns = selectColumns.toSeq

Console.out.println(Console.RED + "Common Columns    - " + selectColumnsList.toSeq + Console.RESET)

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

Console.out.println(Console.WHITE + " -*- diffCondition -*- " + diffCondition + Console.RESET)


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

val diffDF = l.join(r, joinCondition, "fullouter").select((diffCondition +: changeColumn) ++ diffColumns: _*)

Console.out.println(Console.RED + " -*- COMPLETED Diff Operation -*- " + Console.RESET)
Console.out.println(Console.MAGENTA_B + " Diff count = " + diffDF.count() + Console.RESET)

diffDF.groupBy(diffcolumnName).count().show()


//spark-shell --driver-memory 20G --executor-memory 50G --executor-cores 20 -i DiffApp/clinicalencounter.scala



 diffDF.where($"DiffStatus" =!= "NoChange").show(20, false)

diffDF.where($"DiffStatus" =!= "NoChange").orderBy($"patientid").show(20, false)
diffDF.where($"DiffStatus" =!= "NoChange").groupBy($"datasrc").count().show(100, false)
