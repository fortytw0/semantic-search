FROM huggingface/transformers-pytorch-cpu:latest


RUN apt-get update && apt-get install -y \
    wget

RUN pip install pandas numpy sentence-transformers redis

RUN mkdir /search

WORKDIR /search

# Run the code
CMD ["/bin/bash"]