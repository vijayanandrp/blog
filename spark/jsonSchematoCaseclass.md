# Approach to generate case Classes from the Complex Nested JSON Schema in Spark

I worked in the Big Data Projects which does the ETL (Extract-Transform-Load) jobs from Oracle RDBMS to big data ecosystem (Spark, HDFS and Hive). Doing an ETL for lots of clients isn't a easy task. You have to do lots for Oracle ETL query conversion to Spark query. You need to convert the functions that are in-built and custom, apparently you have to write UDF functions to handle it. So doing all these type of work we need a framework to maintain code, run unit testcases and scripts to validation. In the framework I mentioned, `case class` plays an important role during the extraction and validation especially handling the parquet files. 
> case class is the meta-data for the tables or data files that we are dealing. 
> Usally it contains the field (column) name and its datatype
> case class makes the spark to understand the type of data is present in the column
> Thus Explicit Schema definition is acheived

Generating `case class` for an relational database tables are easier and straight way. Say example if you have an `table Employee with columns firstname, middlename, lastname, gender and age`.
The sample case class looks like this 
```scala
case class Employee(
                    firstname:String,
                    lastname:String,
                    middlename:String,
                    age:Integer,
                    gender:String
                )
```

As long as you deal with the flat tables, you dont have to put too much efforts in the case class conversions. 

##### What if Complex Nested JSON Parquet files are given as the input table ? In that case how do create the case classes for struct types and array types ? 

It is very tough and tedious job ever to be done. yeah I faced one.

#### Following are the ways I did to create 100's of case class from an nested JSON File

##### 1. Don't get panic.
I know its boring one but if you follow the points I said it would solve your problem in few minutes
##### 2. First read the JSON file and create the Json schema from it
I have used the `spark-shell` for my convenience 
```scala
import spark.implicits._
 import org.apache.spark.sql.types.{DataType, StructType}
 
val jsonPath = "/user/anonymous/Audit.json"
val jsonDF = spark.read.option("multiline",true).json(jsonPath)

val schemaJson = jsonDF.schema.json
// schema Json string to StructType 
val newSchema = DataType.fromJson(schemaJson).asInstanceOf[StructType]
```
##### 3. Add the custom function to convert the schema to case classes
source - https://gist.github.com/frne/391b809e3528efe6aac718e1a64f4603 (credit)
```scala
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
```
##### 4. Call the convertor function and store the output to your local
so,
```scala
 val x = Schema2CaseClass.schema2Cc(newSchema, "MyClass")
 
 import java.io.PrintWriter

 new PrintWriter("case_class.scala") { write(x); close }
```
##### 5. Use the Python to merge all the same case class to a single case class
Run this script in a `python3` to do the operation, this will remove duplicate fields also

```python
import re

file_path = 'case_class.scala'

fp =  open(file_path).readlines()

fp = " ".join(fp)

group = re.findall('case class(.*?)\(', fp)

# print(group, len(group), len(set(group)))
group = list(set(group))
group.sort()
group = [_.strip() for _ in group if _.strip()]
case_dict = dict()
# print(fp)
for case in group:
    case = case.strip()
    # print(case, re.findall('case class {0} \((.*?)\)'.format(case), fp, re.DOTALL))
    if case not in case_dict.keys():
        case_dict[case] = ", ".join(re.findall('case class {0} \((.*?)\)'.format(case), fp, re.DOTALL)).replace('\n', '')
    else:
        case_dict[case] += ", ".join(re.findall('case class {0} \((.*?)\)'.format(case), fp, re.DOTALL)).replace('\n', '')

# print(case_dict.keys())
fw = open("parse_case_class.scala", "w")
for case in group:
    if case not in case_dict.keys():
        print("Case ", case,  " is missing.")
        continue

    fields = case_dict[case]
    fields  = [field.replace("type :", "typed :").strip()  for field in fields.split(",") if field.strip()]
    fields = list(set(fields))
    fields.sort()
    value = "case class {0} ( {1} ) \n".format(case, ", ".join(fields))
    fw.write(value)
fw.close()
```

### Final words

The above the steps are one way to solve the problem. Still I have faced the circular references of pointing one case class and another. I have removed those manually. 

Hope this would have helped to create case classes from complex nested JSON files.

*Cheers*
