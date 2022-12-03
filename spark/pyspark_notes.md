## Read with partition locally  using basepath

```python
df=spark.read.option("basePath", "data/c4/dfa/c4_dcm_taxonomy_report/").parquet(all_files)
df.printSchema()
df.dtypes
```
