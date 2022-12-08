import sys
import os
import numpy as np
import pandas as pd
import redis
from sentence_transformers import SentenceTransformer, util
import torch
import json
import time

redis_client = redis.Redis('redis' , 6379)

model = SentenceTransformer('all-mpnet-base-v2')
embeddings = torch.tensor(np.load('./embeddings/RC_2022-06.npy'))

with open('./permalinks/RC_2022-06_permalink', 'r') as f:
    permalinks = f.readlines()[0].replace('[', '').replace(']', '').split(',')

while True : 

    job_name = redis_client.rpop('filtered')
    if job_name is not None : 
        job_name = job_name.decode('utf-8')

        redis_client.set(job_name , 'searching')
        search_params = json.loads(redis_client.hget('filtered_job_details' , job_name))

        print('received search params...')
        search_string = search_params['search_string']
        permalinks_to_search = search_params['permalinks']

        print('Creating Target Embeddings...')
        target_embeddings = embeddings[[permalinks.index(pl) for pl in permalinks_to_search]]
        print('target embedding shape : ' , target_embeddings.shape)

        query_embedding = model.encode(search_string)
        print('Creating query embedding : ' , query_embedding.shape)

        batch_size = 5000
        cosine_similarity = [] 

        for i in range(0, query_embedding.shape[0] , batch_size):
            if query_embedding.shape[0] - i < batch_size:
                start = i 
                end = abs(i-query_embedding.shape[0]) + i 
            else:
                start = i 
                end = i + batch_size

                cosine_similarity += util.cos_sim(query_embedding , target_embeddings[start:end , :])[0]

        cosine_similarity = sorted(list(zip(permalinks_to_search , cosine_similarity)) , key=lambda x : x[1] , reverse=True)

        print(cosine_similarity[:10])

        redis_client.lpush('searched', job_name)
        redis_client.set(job_name , 'searched')
        redis_client.hset('searched_job_details' , job_name , json.dumps(cosine_similarity))

    time.sleep(10)

