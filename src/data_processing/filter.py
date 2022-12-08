from pyspark.sql import SparkSession
from pyspark.sql.functions import * 
import redis
import json
import time

'''
1. Setting session information
'''

spark = SparkSession.builder.getOrCreate()
data_files  = 'data/*_PROCESSED'
reddit_df = spark.read.json(data_files)
redis_client = redis.Redis('redis' , 6379)


'''
2. Function Definition
'''

def filter_on_keywords(filter_keywords) : 

    result = None 
    for kw in filter_keywords : 
        kw = ' {} '.format(kw.lower().strip())
        if result is None : 
            result = reddit_df.filter(reddit_df.body_lowercase.contains(kw))
        else : 
            result = result.union(reddit_df.filter(reddit_df.body_lowercase.contains(kw)))
    return result

def filter_on_subreddit(processed_df , subreddits) : 

    rows = processed_df.subreddit.isin(subreddits)
    processed_df = processed_df.filter(rows)
    return processed_df

def remove_duplicate_comments(processed_df) : 
    pass

def filter_on_permalink(permalinks) : 
    rows = reddit_df.permalink.isin(permalinks)
    processed_df = reddit_df.filter(rows)
    return processed_df


def get_top_k_comments(permalink_cosine_similarities , k=100) : 

    permalinks = []
    cosine_similarities  = []

    for i in range(k) : 
        permalink , cosine_similarity = permalink_cosine_similarities[0] , permalink_cosine_similarities[1]
        permalinks.append(permalink)
        cosine_similarities.append(cosine_similarity)

    processed_df = filter_on_permalink(permalinks)
    processed_df = processed_df.withColumn('cosine_similarity' , cosine_similarities)

    return processed_df

'''
3. Main Loop.
'''

start_new_task = True # start new task or collate finished task?

while True : 
    

    if start_new_task : 

        job_name = redis_client.rpop('queued')
        if job_name is not None : 
            job_name = job_name.decode('utf-8')

            search_params = json.loads(redis_client.hget('queued_job_details' , job_name))
            redis_client.set(job_name , 'filtering')

            search_string = search_params['search_string'].split(',')
            subreddits = search_params['subreddits'].split(',')
            filter_keywords = search_params['filter_keywords'].split(',')

            print('search_string : ' , search_string)
            print('subreddits : ' , subreddits)
            print('filter_keywords : ' , filter_keywords)

            processed_df = filter_on_keywords(filter_keywords)
            processed_df = filter_on_subreddit(processed_df , subreddits)

            print('Finished processing data...')

            permalinks = list(processed_df.select('permalink').toPandas()['permalink'])

            search_criteria = {'search_string' : search_string , 'permalinks' : permalinks}

            print('search_criteria : ' , search_criteria)

            redis_client.lpush('filtered', job_name)
            redis_client.set(job_name , 'filtered')
            redis_client.hset('filtered_job_details' , job_name , json.dumps(search_criteria))

        start_new_task = False

    else : 

        job_name = redis_client.rpop('searched')
        if job_name is not None : 
            job_name = job_name.decode('utf-8')
            redis_client.set(job_name , 'finishing')

            search_results = json.loads(redis_client.hget('searched_job_details' , job_name))

            print('Got the following search result : ' , search_results)

            processed_df = get_top_k_comments(search_results)
            results = processed_df.rdd.map(lambda row: row.asDict()).collect()

            print('collated search results : ' , results)

            redis_client.lpush('finished', job_name)
            redis_client.set(job_name , 'finished')
            redis_client.hset('finished_job_details' , job_name , json.dumps(results))

        start_new_task = True

    time.sleep(10)


