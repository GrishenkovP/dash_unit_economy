FROM python:slim-buster

LABEL maintainer="Developer"
LABEL version="1.0"
LABEL description="Дашборд для отображения основных показателей юнит-экономики"

WORKDIR /app 

RUN pip install --upgrade pip

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8050

