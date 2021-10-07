CELERY_BEAT_SCHEDULE = {
    'add': {
        'task': 'tasks.add',
        'schedule': 3,
        'args': (16, 16)
    }
}
