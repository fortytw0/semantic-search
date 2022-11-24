'''
python script to get embeddings for a the reddit data.
the reddit data has been data processed.

there will be a worker class

might use different embeddings


'''
import os
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.functions import col

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct

from pyspark.sql.types import ArrayType, FloatType
from pyspark.ml.linalg import Vectors, VectorUDT

from sentence_transformers import SentenceTransformer

import glob

from tqdm import tqdm

from pathlib import Path

import argparse


def get_parser(
    parser=argparse.ArgumentParser(
        description="to get embeddings for the reddit data"
    ),
):
    parser.add_argument(
        "--input",
        type=Path,
        default="reddit_data",
        help="the input directory that stores the reddit data",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default="reddit_embeddings",
        help="the output directory that stores the embeddings",
    )
    return parser


def get_embeddings(args):
    # detect if the output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # NLP model
    model = SentenceTransformer('bert-base-uncased')

    # get embbeding function
    get_embeddings_udf = udf(lambda body : Vectors.dense(model.encode(body)), VectorUDT())

    # do the for loop for each file
    # for file in tqdm(glob.glob("/content/RC_*")):
    #     print('logging, start to get word embeddings for file: ', file)
    #     # load the data
    #     spark = SparkSession \
    #             .builder \
    #             .appName("sample") \
    #             .config("spark.driver.memory", "12g") \
    #             .getOrCreate()
        
    #     reddit_df = spark.read.json(file)

    #     # get the embeddings
    #     reddit_df = reddit_df.withColumn("embeddings", get_embeddings_udf(col("body")))
    #     print('finish get the embeddings')

    #     # save the data
    #     # reddit_df.write.json(file+'_with_embeddings')
    #     print('logging: finish writing parquet file')

    #     # delete the spark session
    #     spark.stop()
    #     print('logging: close the pyspar session')


    #  print('logging, start to get word embeddings for file: ', file)
        # load the data
    file = '/content/RC_2022-06'
    spark = SparkSession \
            .builder \
            .appName("sample") \
            .config("spark.driver.memory", "12g") \
            .getOrCreate()
    
    reddit_df = spark.read.json(file)

    # get the embeddings
    reddit_df = reddit_df.withColumn("embeddings", get_embeddings_udf(col("body")))
    print('finish get the embeddings')

    # save the data
    reddit_df.write.json(file+'_with_embeddings')
    # print(reddit_df.count())
    print('logging: finish writing parquet file')

    # delete the spark session
    spark.stop()
    print('logging: close the pyspar session')

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    get_embeddings(args)