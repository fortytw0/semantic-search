FROM python:3.8-buster

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y  apt-utils python3-dev python3-setuptools \
                        gcc libc-dev \
                        libffi-dev libssl-dev musl-dev && \
    pip install --upgrade pip

COPY requirements.txt /requirements.txt

RUN pip install --no-cache -r /requirements.txt && \
    useradd -s /bin/bash user && \
    mkdir /api_endpoint

USER user

WORKDIR /api_endpoint

CMD ["/bin/bash"]
