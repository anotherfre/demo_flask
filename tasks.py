from celery import Celery
from zhiHuHot import *
from celery.schedules import crontab

brokers = 'redis://192.168.76.128:6379/0'
backend = 'redis://192.168.76.128:6379/1'

app = Celery('tasks', broker=brokers, backend=backend)

# app.config_from_object('celery_config')
app.conf.beat_schedule = {
    "task_10s": {
        "task": "tasks.zhihu_task",
        "schedule": crontab(hour=21),
        # "args": (10, 10)
    }
}


@app.task
def zhihu_task():
    try:
        zhihu = ZhihuHot()
        html = zhihu.download_item()
        items = zhihu.clear_item(html)
        result = zhihu.save_item(items)
        if result:
            return 'zhihu_hot spider successful'
        else:
            return 'zhihu_hot spider failed'
    except Exception as e:
        print(e)
        return 'error' + str(e)


@app.task
def add(x, y):
    return "my task result: ", x + y
