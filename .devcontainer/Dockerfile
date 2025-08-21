FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin

COPY . .

RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt