# Real-estate lead automation
# Dependencies
wsgi= gunicorn 20.1.0
web = flask_2.0.2
worker = celery_5.2.3 
message_broker = redis_6.0.16
storage_location = ./storage
browser = firefox 97.0.1
webdriver= geckodriver 30.x
database = mongodb atlas free tier
https_tunnel=ngrok

Mongodb collection:
        - Site
        - leads

Installation:

git clone https://github.com/subburajan-perumal/lead_automation.git

cd lead_automation

git fetch

git checkout origin/release_2.1

source genv/bin/activate

pip install -r requirements.txt

set ssl certifcate and key in gunicorn.conf.py
//certfile=<certificatefile>
//keyfile=<keyfile>


#start server and worker:
        terminal 1: gunicorn -c gunicorn
        terminal 2: celery -A app.celery worker -l info -c 1 -Q default,lead,celery -n leadworker@%h -f logs/%n-%i.log
        terminal 3: celery -A app.celery worker -l info -c 2 -Q default,browser,celery -n selenium_worker@%h -f logs/%n-%i.log
        terminal 4: celery -A app.celery flower

#start ngrok for https tunnel
        - cmd: ngrok authtoken <authkey>
        - cmd: ./ngrok http 443

#zoho crm 
        -settings-> workflow Rules  
        -search for production workflow
        -view configuration of workflow 
        -click instance action
        -place the new ngrok link