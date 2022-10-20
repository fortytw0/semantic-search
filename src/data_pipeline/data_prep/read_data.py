from pyspark.sql import SparkSession

import time

spark = SparkSession \
    .builder \
    .appName("SemanticSearch") \
    .getOrCreate()

start_time = time.time()

reddit_df = spark.read.option("multiLine" , "true").json("data/RC_2022-06")

reddit_df.printSchema()

reddit_df = reddit_df.dropDuplicates(['id'])

reddit_df.head(10)

print("Process took : {} seconds".format(time.time() - start_time))


