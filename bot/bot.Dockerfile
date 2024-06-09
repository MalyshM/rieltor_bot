# Backend
FROM python:3.10 as backend

ENV PYTHONUNBUFFERED 1

WORKDIR /
COPY . /bot
RUN pip install --no-cache-dir -r /bot/requirements.txt