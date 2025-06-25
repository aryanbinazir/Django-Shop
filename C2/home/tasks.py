from celery import shared_task
from bucket import bucket
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


#todo: can be async?
def get_all_objects_tasks():
    result = bucket.get_objects()
    return result

@shared_task
def delete_object_task(key):
    bucket.delete_object(key)

@shared_task
def download_object_task(key):
    bucket.download_object(key)