import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from .models import OtpCode
from django.utils import timezone
from datetime import timedelta
from celery import shared_task
from random import randint


@shared_task
def clear_expired_otps():
    time_expire = timezone.now() - timedelta(minutes=2)
    otps_objs = OtpCode.objects.filter(created_on__lt=time_expire)
    otps_objs_count = otps_objs.count()
    otps_objs.delete()
    return f"{otps_objs_count} otps succifully deleted!"

@shared_task
def sum():
    return 'hello world'