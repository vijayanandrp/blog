```python
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.sql.files.maxPartitionBytes", 134217728*2) # 256 MB
spark.conf.set("spark.sql.inMemoryColumnarStorage.compressed", true)
spark.conf.set("spark.sql.inMemoryColumnarStorage.batchSize",10000)
spark.conf.set("spark.sql.cbo.enabled", true)
spark.conf.set("spark.sql.shuffle.partitions",30)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold",10485760)
# Spark 3.0
spark.conf.set("spark.sql.adaptive.enabled",true)
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled",true)
spark.conf.set("spark.sql.adaptive.skewJoin.enabled",true)
```


**1. Serialization** <br>
Serialization plays an important role in the performance for any distributed application. 
By default, Spark uses Java serializer.
Spark can also use another serializer called ‘Kryo’ serializer for better performance.
Kryo serializer is in compact binary format and offers processing 10x faster than Java serializer. <br>
To set the serializer properties:
`conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")`

**2. Advance Variable** <br>
Broadcasting plays an important role while tuning Spark jobs. <br>
Broadcast variable will make small datasets available on nodes locally. <br>
When you have one dataset which is smaller than other dataset, Broadcast join is highly recommended. <br>
To use the Broadcast join: `(df1. join(broadcast(df2)))` <br>

**3. Persisting & Caching data in memory** <br>
Spark persisting/caching is one of the best techniques to improve the performance of the Spark workloads.  <br>
Spark Cache and Persist are optimization techniques in DataFrame / Dataset for iterative and interactive Spark applications to improve the performance of Jobs. <br>

Using cache() and persist() methods, Spark provides an optimization mechanism to store the intermediate computation of a Spark DataFrame
so they can be reused in subsequent actions. <br>

When you persist a dataset, each node stores it’s partitioned data in memory and reuses them in other actions on that dataset. 
And Spark’s persisted data on nodes are fault-tolerant meaning if any partition of a Dataset is lost, 
it will automatically be recomputed using the original transformations that created it. <br>

`df.where(col("State") === "PR").cache()`  <br> <br>

**4. Use coalesce() over repartition()**  <br>
When you want to reduce the number of partitions prefer using coalesce() as it is an optimized or improved version of repartition() 
where the movement of the data across the partitions is lower using coalesce which ideally performs better when you dealing with bigger datasets.

Note: Use repartition() when you wanted to increase the number of partitions.  <br> <br>

# References  <br>
1. https://www.syntelli.com/eight-performance-optimization-techniques-using-spark
2. https://sparkbyexamples.com/spark/spark-sql-performance-tuning-configurations/
3. https://sparkbyexamples.com/spark/spark-performance-tuning/
4. https://spark.apache.org/docs/latest/sql-performance-tuning.html
