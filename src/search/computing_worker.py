'''
The computing worker that takes indicies as input, compute the similarity matrix, and return the result to the master.


questions and quesitons:

1. we might need to think a uniform way to encode/decode redis messages.

'''


import sys
import os
import numpy as np
import pandas as pd
import redis
import torch
import torch.nn.functional as F
from torch.nn import CosineSimilarity
import logging


def load_embeddings():
    # Read the embedding file
    return torch.tensor(np.load('./RC_2022-06.npy'))


def load_permalinks():
    # Read the list of permalinks
    with open('./RC_2022-06_permalink', 'r') as f:
        p_list = f.readlines()[0].replace('[', '').replace(']', '').split(',')
    return p_list


def compute_similarity(input_embedding, embeddings, partial_permalink_list, all_permalink_list):
    # construct embedding matrix based on the permalinks
    reverse_dict = dict(zip(all_permalink_list, range(len(all_permalink_list)))) # construct a reverse dict, key: permalink, value: index
    index_list = [reverse_dict[permalink] for permalink in partial_permalink_list] # get the index list
    partial_embeddings = embeddings[index_list] # get the embedding matrix based on the index list


    # Compute the cosine similarity between the input and the embeddings
    cosine = CosineSimilarity(dim=1, eps=1e-6)
    
    # Split the embeddings matrix into chunks
    chunk_size = 500000
    chunks = torch.chunk(partial_embeddings, chunk_size)
    
    # Compute the cosine similarity for all chunks in a single pass
    cosine_result = []
    for chunk in chunks:
        output = cos(chunk, input_embedding)
        cosine_result.append(output)
    top10 = torch.cat(cosine_result).topk(10)

    # get index of the top 10
    top10_index = top10.indices.tolist()

    # get the permalink of the top 10
    top10_permalink = [partial_permalink_list[index] for index in top10_index]

    return top10_permalink 


def main():
    # Connect to the redis server
    redisHost = os.getenv("REDIS_HOST") or "localhost"
    redisPort = os.getenv("REDIS_PORT") or 6379
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    
    # Configure the logger
    logging.basicConfig(filename='worker.log', level=logging.DEBUG)

    # Load the embeddings and permalinks
    embeddings = load_embeddings()
    p_list = load_permalinks()
    p_pd = pd.DataFrame(p_list, columns=['permalink'])

    while True:
        try:
            # Listen to the redis
            permalink_str = redisClient.blpop("permalinks", timeout=0)[1].decode("utf-8")
            input_str = redisClient.blpop("input", timeout=0)[1].decode("utf-8")
            logging.debug('Received permalinks and input')
            
            # Decode the user's input
            input_embedding = model.encode(input_str)
            logging.debug('Encoded the input')

            permalink_list = [str(i) for i in permalink_str.strip('[]').split(',')]
            top10_permalink = compute_similarity(input_embedding, embeddings, permalink_list, p_list)
            logging.debug('Computed the similarity')

            # Return the result to the master
            result = str(top10_permalink) # it might need another way to decode the result
            logging.debug(f'Returning result: {result}')
            redisClient.rpush("result", result)
        except Exception as e:
            logging.exception(e)
            continue

if __name__ == "__main__":
    main()


