import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

data_files = sys.argv[1]

print('Received Data File : ' , data_files)

spark = SparkSession.builder.getOrCreate()

reddit_df = spark.read.json(data_files)

reddit_df = reddit_df.withColumn('body_lowercase' , F.lower(F.col("body")))



reddit_df.write.json(data_files+'_PROCESSED')
