FROM ubuntu:latest

RUN apt-get update && \
    apt-get -y install \
        python3 \
        python3-pip \
        sqlite

RUN mkdir -p /tmp
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

LABEL maintainer="Vijay Ullal <ullal.vijay@gmail.com>"

ENTRYPOINT ["python3", "main.py"]