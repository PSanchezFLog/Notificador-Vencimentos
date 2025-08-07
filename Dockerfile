FROM ubuntu:24.04

RUN apt update && apt upgrade -y && \
    apt install -y nano python3-full python3-pip && \
    pip3 install --break-system-packages pandas python-dotenv schedule flask


COPY . /home