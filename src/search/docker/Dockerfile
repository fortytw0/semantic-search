FROM pytorch/pytorch:1.8.1-cuda11.0-cudnn8-runtime

RUN apt-get update && apt-get install -y \
    wget

RUN pip install pandas numpy sentence-transformers redis

RUN mkdir /search

WORKDIR /search

# Run the code
CMD ["/bin/bash"]