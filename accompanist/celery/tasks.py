from accompanist.celery.main import app
import time


@app.task
def add(x, y):
    time.sleep(5)
    return x + y
