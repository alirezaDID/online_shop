import os
from celery import Celery
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


app = Celery('core', include=['Account.tasks'])  

app.autodiscover_tasks()