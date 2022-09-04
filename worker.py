import os
import time

from celery import Celery

from celery_app.app import init_tasks

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL",
    "redis://localhost:6379",
)
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND",
    "redis://localhost:6379",
)
init_tasks(celery)
