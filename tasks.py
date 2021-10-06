import time
from celery import Celery

brokers = 'redis://192.168.11.128:6379/0'
backend = 'redis://192.168.11.128:6379/1'

app = Celery('tasks', broker=brokers, backend=backend)


@app.task
def add(x, y):
    time.sleep(3)
    return x + y
