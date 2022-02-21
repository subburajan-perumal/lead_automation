FROM python:3.9.10-slim-buster

RUN mkdir /opt/app
RUN pip install -U pip
WORKDIR /opt/app
EXPOSE 5000
COPY requirements.txt /opt/app/requirements.txt

RUN  pip install -r requirements.txt

COPY . /opt/app/

CMD [ "python","run.py" ]
# CMD [ "gunicorn","-b 0.0.0.0:5000 run:app" ]