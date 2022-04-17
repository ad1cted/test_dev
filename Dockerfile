# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code/app
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . /code/
