# Processing Large JSON dataset with Spark SQL

Spark SQL offers built-in support, like JSON, parquet, XML, CSV, text files, and other numbers of data formats. 
Each new release of the Spark version contains various improvements in the API that make use of JSON data more convenient and efficient.

JavaScript Object Notation (JSON) format is a very basic file readable for humans, and convenient to use. 
But its simplicity, since it's schema-less, can lead to problems. 
Such services can return insane JSON responses containing integer numbers as strings, or encode `nulls` in different ways, such as `null`, `""`, or even `"null"`, 
particularly when you have to deal with unreliable third-party data sources.

Assuming you have an access to spark tools like `spark-shell` to execute the below commands.

## Loading data

You can read and JSON directly from files like HDFS or S3 bucket path to DataFrame:

##### Example for S3
```scala
val df = spark.read.json("s3a://datastore/files/json/some-file.json")
```

##### Example for HDFS
```scala
val df = spark.read.json("/datastore/files/json/some-file.json")
```

To be noted - Spark assumes each line to be a separate JSON object, so it will fail if you’ll try to load a pretty formatted JSON file.
In that case, you can opt for the `multiline` option to avoid the corrupt record problem while reading JSON files.

```scala
val df = spark.read.option("multiline", "true").json("s3a://datastore/files/json/some-file.json")
```

Also you read JSON data from RDD[String] object like:

##### Example 1
```scala
// construct RDD[Sting]
val events = sc.parallelize("""{"action":"create","timestamp":"2020-10-13T00:01:17Z"}""" :: Nil)

// read it
val df = spark.read.json(events)
```
##### Example 2
```scala
// Alternatively, a DataFrame can be created for a JSON dataset represented by
// a Dataset[String] storing one JSON object per string
val peopleDataset = spark.createDataset(
                 """{"name":"Vijay","address":{"city":"Bengaluru","state":"Karnataka"}}""" 
                 :: Nil)

val peopleDf = spark.read.json(peopleDataset)
```


## Schema Inference and Explicit Schema definition

By hitting `spark.read.json(events)` will not load data, since DataFrames are evaluated lazily.
But it will trigger schema inference, the spark will go over RDD to determine schema that fits the data.

In the spark-shell you can print schema using printSchema method:

```
scala> df.printSchema()
root
 |-- action: string (nullable = true)
 |-- timestamp: string (nullable = true)
 ```
 
As you saw in the last example Spark by default inferred type of both columns as strings similarly spark does the same for all strcut and arry types.

It is possible to provide schema explicitly to avoid that extra scan. This eventually helps to improve the reading performance for larger files:

```scala
val schema = (new StructType).add("action", StringType).add("timestamp", TimestampType)

val df = spark.read.schema(schema).json(events)

df.show(false)

// +------+--------------------+
// |action|           timestamp|
// +------+--------------------+
// |create|2016-01-07 01:01:...|
// +------+--------------------+
```

As you might have noticed type of `timestamp` column is explicitly forced to be a `TimestampType`.
It’s important to understand that this type coercion is performed in JSON parser, 
and it has nothing to do with DataFrame's type casting functionality. 
Type coercions implemented in parser are somewhat limited and in some cases unobvious. 

Following example demonstrates it:
```scala

val events = sc.parallelize(
  """{"action":"create","timestamp":1452121277}""" ::
  """{"action":"create","timestamp":"1452121277"}""" ::
  """{"action":"create","timestamp":""}""" ::
  """{"action":"create","timestamp":null}""" ::
  """{"action":"create","timestamp":"null"}""" ::
  Nil
)

val schema = (new StructType).add("action", StringType).add("timestamp", LongType)

spark.read.schema(schema).json(events).show(false)

// +------+----------+
// |action| timestamp|
// +------+----------+
// |create|1452121277|
// |  null|      null|
// |create|      null|
// |create|      null|
// |  null|      null|
// +------+----------+
```

Frankly, that is not a result that one can expect. 
**Look at 2nd row in the result set, as you may see, there is no conversion from string to an integer.**
But here is one more big problem, if you try to set type for which parser doesn’t have conversion, 
it won’t simply discard value and set that field to `null`, instead, it will consider the entire row as incorrect, and set all fields to `null`s. 
The good news is that you can read all values as strings.

**It is always better to read the JSON file as it is, default convert most columns to stringType first.
After that run Type Casting to avoid data loss from parser's direct conversion as shown above.**

### Example of Type Casting
If you can’t be sure in a quality of you data, the best option is to explicitly provide schema forcing `StringType` 
for all untrusted fields to avoid extra RDD scan, and then cast those columns to desired type:

```scala
val schema = (new StructType).add("action", StringType).add("timestamp", StringType)

spark.read.schema(schema).json(events).select($"action", $"timestamp".cast(LongType)).show(false)

// +------+----------+
// |action| timestamp|
// +------+----------+
// |create|1452121277|
// |create|1452121277|
// |create|      null|
// |create|      null|
// |create|      null|
// +------+----------+
```

Now that’s more like a sane result.

Spark’s catalyst optimizer has a very powerful type casting functionality, 
let’s see how we can parse UNIX timestamps from the previous example:

```scala
val schema = (new StructType).add("action", StringType).add("timestamp", StringType)

spark.read.schema(schema).json(events).select($"action", $"timestamp".cast(LongType).cast(TimestampType)).show(false)

// +------+--------------------+
// |action|           timestamp|
// +------+--------------------+
// |create|2016-01-07 00:01:...|
// |create|2016-01-07 00:01:...|
// |create|                null|
// |create|                null|
// |create|                null|
// +------+--------------------+
```

## Handling nested objects

Often in API responses, useful data might be wrapped in several layers of nested objects:

```json
{
  "payload": {
    "event": {
      "action": "create",
      "timestamp": 1452121277
    }
  }
}
```

Star (\*) expansion makes it easier to unnest with such objects, for example:

```scala
val vals = spark.createDataset(
          """{"payload":{"event":{"action":"create","timestamp":1452121277}}}""" 
          :: Nil)

val schema = (new StructType)
  .add("payload", (new StructType)
    .add("event", (new StructType)
      .add("action", StringType)
      .add("timestamp", LongType)
    )
  )

spark.read.schema(schema).json(vals).select($"payload.event.*").show(false)

// +------+----------+
// |action| timestamp|
// +------+----------+
// |create|1452121277|
// +------+----------+
```

If you need more control over column names, you can always use as method to rename columns, e.g.:

```scala
spark.read.schema(schema).json(vals)
  .select(
    $"payload.event.action".as("event_action"),
    $"payload.event.timestamp".as("event_timestamp")
  ).show(false)

// +------------+---------------+
// |event_action|event_timestamp|
// +------------+---------------+
// |      create|     1452121277|
// +------------+---------------+

```
## Converting Large JSON files to Parquet 

Source - https://garrens.com/blog/2017/10/09/spark-file-format-showdown-csv-vs-json-vs-parquet/
Source - https://garrens.com/blog/2017/06/26/real-time-big-data-analytics-parquet-and-spark-bonus/

*Parquet is optimized for the Write Once Read Many (WORM) paradigm. 
It’s slow to write, but incredibly fast to read, especially when you’re only accessing a subset of the total columns.
It is a compressible binary columnar data format used in the Hadoop ecosystem.*

1. Binary means parquet files cannot be opened by typical text editors natively (sublime text, vim, etc).
2. Columnar means the data is stored as columns instead of rows as most traditional databases (MySQL, PostgreSQL, etc) 
   and file formats (CSV, JSON, etc). 
3. Compressed means the file footprint on disk (HDFS, S3, or local filesystem) is smaller than a typical raw uncompressed file. 
   Parquet handles compression differently than traditional compression of a CSV file for example, but in a similar vein to Avro.
4. Use snappy compression if storage space is not a concern due to it being splittable, 
   but for what should be a relatively small performance hit but much better compression, use gzip. 
   
For use cases requiring operating on entire rows of data, a format like CSV, JSON, or even AVRO should be used.


### JSON
Named columns | Inferred types | EAGERLY evaluated

```scala
val df = spark.read.json("data.json")
df.printSchema
root
 |-- alphanum: string (nullable = true)
 |-- epoch_date: long (nullable = true)
 |-- guid: string (nullable = true)
 |-- name: string (nullable = true)
 ```
Like the eagerly evaluated (for schema inferencing) CSV, JSON files also are eagerly evaluated.

### Parquet
Named Columns | Defined types | lazily evaluated

```scala
val df = spark.read.parquet("data.parquet")
df.printSchema
root
 |-- alphanum: string (nullable = true)
 |-- date: long (nullable = true)
 |-- guid: string (nullable = true)
 |-- name: string (nullable = true)
```

Unlike CSV and JSON, Parquet files are binary files that contain metadata about their contents, 
so without needing to read/parse the content of the file(s), Spark can just rely on the header/metadata inherent to Parquet to determine column names and data types.

Use Apache Parquet instead of CSV or JSON whenever possible, because it’s faster and better.

### How Parquet helps in processing large JSON files?
Reading rows-stored JSON files directly and processing them through DataFrames has lots of limitations and drawbacks. 
JSON is slow to parse because it requires reading all of the rows in the entire file, parsing each line’s columns.

If those limitations had you cringing, I’ve made my case well :). There is an alternative that utilizes SParquet…

1. Process the JSON files into Parquet files (snappy or gzip-compressed)
2. Use Spark with those Parquet files to drive a powerful and scalable analytics solution

Parquet wins in reading, filtering, aggregating (group by) over JSON.

### Use the right compression for files
The types of files we deal with can be divided into two types

1. Splittable ( eg. lso, bzip2, snappy)
2. Non-splittable ( eg. gzip, zip, lz4)


For discussion purposes, "splittable files" means that they can be processed in parallel in a distributed manner rather than on a single machine (non-splittable).

## Key Takeaways 

The larger datasets are, the longer you wait. Even if you need only the first record from the file, Spark (by default) reads its whole content to create a valid schema consisting of the superset of used fields and their types. Let’s see how to improve the process with three simple hints.

1. Read large JSON and save it as Parquet file format with snappy compression for faster execution, data validation, and quick metrics.

2. In case of larger JSON to read, use `sampling ratio = 0.1` to read JSON files if you are sure don't want to leave any field or schema is not static, go for the full dataset.

```scala
# JSON
spark.read.options(samplingRatio=0.1).json("sample/json/")
```
3. In case Schema is known and static. It is a better approach to read large JSON files with an explicit schema. Such the parser won't spend much time in analyzing the dynamic content to assign the DataTypes while creating DataFrames.

4. It is better to store the static schema as JSON in an external file and read the schema into a variable before reading large JSON files.
```python
schema_json = spark.read.text("/.../sample.schema").first()[0]
schema = StructType.fromJson(json.loads(schema_json))
```



Hint #1: Use samplingRatio
If your datasets have mostly static schema, there is no need to read all the data. You can speed uploading files with samplingRatio option for JSON and XML readers - the value is from range (0,1] and specifies what fraction of data will be loaded by scheme inferring job.

```python
# JSON
spark.read.options(samplingRatio=0.1).json("sample/json/")
```
**similar option for CSV does not exist :-(**
Now the process of loading files is faster, but it still could be better. What’s more, 
if your code relies on the schema and schema in the files changes (it’s allowed in semi-structured formats), the application may fail.
Spark will not be able to build an execution plan. I faced the problem many times maintaining ETLs based on daily partitioned datasets in JSON.

Hint #2: define the static schema
The solution to these problems already exists in spark codebase - all mentioned DataFrame readers take the schema parameter. If you pass the schema, the Spark context will not need to read underlying data to create DataFrames. Still, defining a schema is a very tedious job…

```python
from pyspark.sql.types import *

# This is a simplified schema of stackoverflow's posts collection
schema = StructType([
    StructField('Id', IntegerType()),
    StructField('AcceptedAnswerId', IntegerType()),
    StructField('AnswerCount', IntegerType()),
    StructField('ClosedDate', TimestampType()),
    StructField('CommentCount', IntegerType()),
    StructField('CreationDate', TimestampType()),
    StructField('FavoriteCount', IntegerType()),
    StructField('LastActivityDate', TimestampType()),
    StructField('OwnerDisplayName', StringType()),
    StructField('OwnerUserId', IntegerType()),
    StructField('ParentId', IntegerType()),
    StructField('Score', IntegerType()),
    StructField('Title', StringType()),
    StructField('ViewCount', IntegerType())
])

# JSON
df = spark.read.json("sample/json/", schema=schema)

# CSV
df = spark.read.csv("sample/csv/", schema=schema, header=True)

# XML
df = spark.read.format("com.databricks.spark.xml") \
       .options(rowTag="post").load("sample/xml/", schema=schema)
```   

Now loading the files is as fast as possible - Spark won’t run any job to create dataframes. For complex datasets schema definition may take even hundreds of code lines and it’s very easy to make a mistake when writing them. The datasets metadata in application code doesn’t really look like an elegant way to handle the problem.

Hint #3: store schemas outside code
Fortunately, schemas are serializable objects and they serialize nicely to python dictionaries using standard pyspark library:

```python
> import json
> print(schema.json())
{"fields":[{"metadata":{},"name":"Id","nullable":true,"type":"integer"},{"metadata":{},"name":"AcceptedAnswerId","nullable":true,"type":"integer"} ...
> print(json.dumps(schema.jsonValue(), indent=2))
{
  "fields": [
    {
      "name": "Id",
      "nullable": true,
      "metadata": {},
      "type": "integer"
    },
    {
      "name": "AcceptedAnswerId",
      "nullable": true,
      "metadata": {},
      "type": "integer"
    },
    ...
}
```
If you paste the JSON output (compressed one, from schema.json()) into the file,
you will be able to re-create schema objects based on the data using the following instructions:

```python
schema_json = spark.read.text("/.../sample.schema").first()[0]
schema = StructType.fromJson(json.loads(schema_json))
```

Using this trick you can easily store schemas on filesystem supported by spark (HDFS, local, S3, …) and load them into the applications using a very quick job.

Getting it all together
=======================
Reading semi-structured files in Spark can be efficient
if you know the schema before accessing the data. But defining the schema manually is hard and tedious…

Next time you are building an ETL application based on CSV, JSON, or XML files, try the following approach:

1. Locate a small, representative subset of input data (so that it contains a superset of possible fields and their types). If you want to be 100% sure that you don’t miss any field, use the whole dataset. For really big but consistent sources consider using samplingRatio parameter.
2. Load the above dataset as dataframe and extract JSON representation of the schema into a file. If you store data on distributed storage like HDFS or S3, it’s good to store this file there, too.
3. In your application add a code that reads the schema file into a variable.
   Load your input dataset passing schema parameter pointing to the variable.
