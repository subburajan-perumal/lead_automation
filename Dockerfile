FROM python:3.9.10-slim-buster

WORKDIR /opt/app

COPY .requirements.txt /opt/app/requirements.txt

RUN  pip install -r requirements.txt

COPY . /opt/app/
