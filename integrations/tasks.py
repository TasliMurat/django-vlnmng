from celery import shared_task
import time


@shared_task
def my_task():
    time.sleep(5)
    return "5 saniye uyudu"