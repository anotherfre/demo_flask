import time
from celery import Celery

brokers = 'redis://192.168.31.196:6379/10'
backend = 'redis://192.168.31.196:6379/14'

app = Celery('proj', broker=brokers, backend=backend)
# app.config_from_object('celery_config')


@app.task
def add(x, y):
    time.sleep(3)
    return x + y
