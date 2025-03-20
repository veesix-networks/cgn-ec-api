ARG BASE_CONTAINER=python:3.12.3-slim

FROM --platform=linux/amd64 $BASE_CONTAINER

LABEL maintainer="cgn-ec@veesix-networks.co.uk"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--forwarded-allow-ips", "*" ]