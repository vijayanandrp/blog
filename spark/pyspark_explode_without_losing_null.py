from pyspark.sql.functions import *

def flatten_df(nested_df):
    flat_cols = [c[0] for c in nested_df.dtypes if c[1][:6] != 'struct']
    nested_cols = [c[0] for c in nested_df.dtypes if c[1][:6] == 'struct']
    flat_df = nested_df.select(flat_cols +
                               [col(nc + '.' + c).alias(nc + '_' + c)
                                for nc in nested_cols
                                for c in nested_df.select(nc + '.*').columns])
    print("flatten_df_count :", flat_df.count())
    return flat_df

def explode_df(nested_df):
    flat_cols = [c[0] for c in nested_df.dtypes if c[1][:6] != 'struct' and c[1][:5] != 'array']
    array_cols = [c[0] for c in nested_df.dtypes if c[1][:5] == 'array']
    for array_col in array_cols:
        schema = new_df.select(array_col).dtypes[0][1]
        nested_df = nested_df.withColumn(array_col, when(col(array_col).isNotNull(), col(array_col)).otherwise(array(lit(None)).cast(schema))) 
    nested_df = nested_df.withColumn("tmp", arrays_zip(*array_cols)).withColumn("tmp", explode("tmp")).select([col("tmp."+c).alias(c) for c in array_cols] + flat_cols)
    print("explode_dfs_count :", nested_df.count())
    return nested_df


new_df = flatten_df(myDf)
while True:
    array_cols = [c[0] for c in new_df.dtypes if c[1][:5] == 'array']
    if len(array_cols):
        new_df = flatten_df(explode_df(new_df))
    else:
        break
    
new_df.printSchema()
