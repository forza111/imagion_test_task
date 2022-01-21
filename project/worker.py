import os

from bs4 import BeautifulSoup
from celery import Celery
from fastapi import HTTPException
import requests


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="create_task")
def create_task(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPException as err:
        raise err
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        result = {}
        for tag in soup.find_all(True):
            if tag.find(True):
                nested = []
                [nested.append(i.name) for i in tag.find_all(True)]
                if not result.get(tag.name):
                    result[tag.name] = {"count": 1, "nested": len(nested)}
                else:
                    result.pop(tag.name)
        return result