<h1 align="center"> Real-estate lead automation</h1>

## Requirements
* WSGI = [gunicorn 20.1.0](https://gunicorn.org/)<br>
Web_Server = [flask_2.0.2](https://flask.palletsprojects.com/en/2.1.x/)<br>
Worker = [celery_5.2.3](https://docs.celeryq.dev/en/stable/)<br> 
Message_broker = [redis_6.0.16](https://redis.io)<br>
Storage_location = ./storage<br>
Browser = firefox 97.0.1<br>
Webdriver= geckodriver 30.x<br>
Database = Mongodb Atlas M0<br>
HTTPS_tunnel = ngrok<br>

## Installation:
### Step 1:
> clone code from   git repo
```sh
git clone https://github.com/subburajan-perumal/lead_automation.git

```

```sh
cd lead_automation
```
> switch to latest branch
```sh
git checkout origin/release_2.1
```

### Step 2:

for activate virtual enivironment
```sh
source genv/bin/activate
```
### Step 3:

install python dependencies
```sh
pip install -r requirements.txt
```
### Step 4:

set ssl certifcate and key file  in gunicorn.conf.py

```py
#gunicorn.conf.py<br>
certfile=certificatefile
keyfile=keyfile
```
### Step 6:

## HTTPS tunnel
```sh
#for first time
$ ngrok authtoken <authkey>


$ ./ngrok http 443
```

## Server 

Start flask server
```sh
$ gunicorn -c gunicorn.conf.py
```


## Experimental worker
```sh
$ genv/bin/celery multi restart  leadworker selenium bulk_leads -E -A app.celery -c 1 -c:selenium 4  -Q:leadworker lead,celery,default -Q:selenium browser,default,celery -Q:bulk_leads bulk,default,celery --pidfile=/run/celery/%N.pid
```


## Start Bulk worker
```
genv/bin/celery -A app.celery worker --loglevel=INFO --concurrency=2 -n bulk_leads@%h
```


## Start Celery Workers
```sh
$ genv/bin/celery multi restart  leadworker selenium -E -A app.celery -c 1 -c:selenium 4  -Q:leadworker lead,celery,default -Q:selenium browser,default,celery --pidfile=/run/celery/%N.pid
```



## Leadworker
Start lead worker
```sh
$ celery -A app.celery worker -l info -c 1 -Q default,lead,celery -n leadworker@%h -f logs/%n-%i.log
```


## Selenium worker
Start selenium worker
```sh
$ celery -A app.celery worker -l info -c 4 -Q default,browser,celery -n selenium_worker@%h -f logs/%n-%i.log
```

## Monitoring tool
Start monitoring tool
```sh
$ celery -A app.celery flower
```


## COMMANDS
Start Flower
```
genv/bin/celery -A app.tasks flower
```

View Flower
```
http://localhost:5555
```

Run tasks
```
genv/bin/celery -A app.tasks call app.tasks.run_apis
```

Check logs
```
cd /var/log/celery/
```

Start Celery Beats
```
celery -A app.tasks beat -l debug
```

<footer>

<footer>