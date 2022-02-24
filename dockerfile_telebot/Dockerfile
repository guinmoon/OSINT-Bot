FROM python:3.8.12-buster

USER root

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt  &&\
    apt update && \
    apt-get install -y nodejs npm