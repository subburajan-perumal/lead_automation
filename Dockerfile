FROM python:3.9.2

ADD . /opt/lead_automation

WORKDIR /opt/lead_automation

RUN pip install -r requirements.txt

CMD ["run.py"]

