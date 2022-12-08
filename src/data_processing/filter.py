from pyspark.sql import SparkSession
from pyspark.sql.functions import * 
import redis
import json
import time

spark = SparkSession.builder.getOrCreate()
data_files  = 'data/*_PROCESSED'
reddit_df = spark.read.json(data_files)

redis_client = redis.Redis('redis' , 6379)

while True : 

    job_name = redis_client.rpop('queued')
    if job_name is not None : 
        job_name = job_name.decode('utf-8')
        print('Found job : ' , job_name)

        search_params = json.loads(redis_client.hget('queued_job_details' , job_name))
        print('Search Params : ' , search_params)

        subreddits = search_params['subreddits']
        filter_keywords = search_params['filter_keywords'].split(',')

        print('Filtering on keywords...')
        result = None 
        for kw in filter_keywords : 
            kw = ' {} '.format(kw.lower().strip())
            if result is None : 
                result = reddit_df.filter(reddit_df.body_lowercase.contains(kw))
            else : 
                result = result.union(reddit_df.filter(reddit_df.body_lowercase.contains(kw)))

        print('Filtering on subreddits...')
        columns = result.subreddit.isin(subreddits)
        result = result.filter(columns)

        print('Extracitng permalinks')
        permalinks = list(result.select('permalink').toPandas()['permalink'])
        print('Number of permalinks : ' , len(permalinks))

        redis_client.lpush('filtered', job_name)
        redis_client.hset('filtered_job_details' , job_name , json.dumps(permalinks))

    time.sleep(10)


