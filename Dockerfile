FROM python:3.9-slim

EXPOSE 80

WORKDIR /app

COPY requirements.txt /app

RUN apt update && apt install -y git && pip3 install -r requirements.txt
