from sentence_transformers import SentenceTransformer
import numpy as np
import time
import json
import glob
import os

#---- User Config ----#

model_name = 'all-mpnet-base-v2'
reddit_data_dir = '/content/RC_2022-06'
reddit_embedding_dir = ''
num_files = 1
samples_per_file = -1 # -1 for all samples in a file 
batch_size = 128



log_file = 'logs/embedding.log'


#---- Loading Sentence Transformer Model ----#

model = SentenceTransformer(model_name)


def encode_reddit_file(src_file, 
                    dest_dir,
                    samples_per_file=-1) : 

    reddit_data = open(src_file)
    file_name = os.path.basename(src_file)
    dest_path = os.path.join(dest_dir , file_name + '.npy')
    reddit_comments = [json.loads(rd)['body'] for rd in reddit_data.readlines() ]

    sample_reddit_comments = reddit_comments[0:samples_per_file]

    start_time = time.time()

    sample_embedding = model.encode(sample_reddit_comments, 
                                    batch_size=batch_size , 
                                    show_progress_bar=True , 
                                    convert_to_numpy=True)
    np.save(dest_path , sample_embedding)

    with open(log_file , 'a') as f : 
        f.write(f'{file_name} Took a total of :  {time.time() - start_time} seconds')

#---- Main ----#


dest_files = [os.path.basename(f).replace('.npy' , '') for f in glob.glob(os.path.join(reddit_embedding_dir , '*.npy'))]
src_files = [f for f in glob.glob(os.path.join(reddit_data_dir , '*')) if os.path.basename(f) not in dest_files]

src_files = src_files[:num_files]

print(src_files)

# for src_file in src_files : 
#     encode_reddit_file(src_file , reddit_embedding_dir)


