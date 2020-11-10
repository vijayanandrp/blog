Source - https://gist.github.com/frne/391b809e3528efe6aac718e1a64f4603

/**
 // Generate Case class from DataFrame.schema
import spark.implicits._
import org.apache.spark.sql.types.{DataType, StructType}

val jsonPath = "/user/anonymous/Audit.json"
val jsonDF = spark.read.option("multiline",true).json(jsonPath)
jsonDF.createOrReplaceTempView("jsonDF")
val schemaJson = jsonDF.schema.json
val newSchema=DataType.fromJson(schemaJson).asInstanceOf[StructType]
val x = Schema2CaseClass.schema2Cc(newSchema, "MyClass")
import java.io.PrintWriter
new PrintWriter("case_class.txt") { write(x); close }

 */

  object Schema2CaseClass {

    import org.apache.spark.sql.types._

    case class RecFieldRes(fieldStr: String, additionalCc: Option[String] = None)

    case class CcRes(cc: String, additional: List[String])

    def schema2Cc(schema: StructType, className: String): String = {
      val res = CcRes(s"case class $className (\n", Nil)
      val res1 = schema.map(field).foldLeft(res)((b, a) => b.copy(b.cc + s"\n${a.fieldStr},", b.additional ++ a.additionalCc))
      res1.cc.stripSuffix(",") + "\n)\n" + res1.additional.mkString("\n\n")
    }

    private def field(sf: StructField): RecFieldRes = {

      def fd: String => String = fieldDef(sf)

      sf.dataType match {
        case at: ArrayType => at.elementType match {
          case s: StructType => RecFieldRes(fd(s"Seq[${sf.name.toLowerCase.capitalize}]"), Some(schema2Cc(s, sf.name.toLowerCase.capitalize)))
          case _ => RecFieldRes(fd(s"Seq[${primitiveFiledType(at.elementType)}]"))
        }
        case mt: MapType => RecFieldRes(fd("Map")) //TODO
        case st: StructType => RecFieldRes(fd(sf.name.toLowerCase.capitalize), Some(schema2Cc(st, sf.name.toLowerCase.capitalize)))
        case pt => RecFieldRes(fd(primitiveFiledType(pt)))
      }
    }

    private def primitiveFiledType(dt: DataType): String = dt match {
      case _: ByteType => "Byte"
      case _: ShortType => "Short"
      case _: IntegerType => "Int"
      case _: LongType => "Long"
      case _: FloatType => "Float"
      case _: DoubleType => "Double"
      case _: DecimalType => "java.math.BigDecimal"
      case _: StringType => "String"
      case _: BinaryType => "Array[Byte]"
      case _: BooleanType => "Boolean"
      case _: TimestampType => "java.sql.Timestamp"
      case _: DateType => "java.sql.Date"
      case _ => "String"
    }

    private def fieldDef(sf: StructField)(ft: String): String = sf match {
      case x if x.nullable && !x.dataType.isInstanceOf[ArrayType] && !x.dataType.isInstanceOf[MapType] =>
        s"  ${sf.name}: Option[$ft]"
      case _ => s"  ${sf.name}: $ft"
    }
  }


  // Generate Case class from DataFrame.schema
 import spark.implicits._
 import org.apache.spark.sql.types.{DataType, StructType}

 val jsonPath = "/user/anonymous/Audit.json"
 val jsonDF = spark.read.option("multiline",true).json(jsonPath)
 jsonDF.createOrReplaceTempView("jsonDF")
 val schemaJson = jsonDF.schema.json
 val newSchema=DataType.fromJson(schemaJson).asInstanceOf[StructType]
 val x = Schema2CaseClass.schema2Cc(newSchema, "MyClass")
 import java.io.PrintWriter
 new PrintWriter("case_class.txt") { write(x); close }
 
