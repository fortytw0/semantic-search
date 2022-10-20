from pyspark.sql import SparkSession

import time

spark = SparkSession \
    .builder \
    .appName("SemanticSearch") \
    .getOrCreate()

start_time = time.time()

reddit_df = spark.read.option("multiline" , "true").json("data/RC_2022-06")

reddit_df.printSchema()

print(reddit_df.count())

reddit_df = reddit_df.dropDuplicates(['id'])

print(reddit_df.head(10))

print(reddit_df.count())

print("Process took : {} seconds".format(time.time() - start_time))


