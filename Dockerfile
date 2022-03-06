FROM python:3.9.10-slim-buster

RUN mkdir /opt/lead_automation
RUN pip install -U pip
WORKDIR /opt/lead_automation
EXPOSE 5000
COPY requirements.txt /opt/lead_automation/requirements.txt
# RUN source genv/bin/activate
RUN  pip install -r requirements.txt

COPY . /opt/lead_automation/
# CMD [ "python","run.py" ]
CMD [ "gunicorn", "-b", "0.0.0.0:5000" ,"run:app"]