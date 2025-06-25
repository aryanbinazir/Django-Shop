from celery import shared_task
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from accounts.models import OtpCode

@shared_task
def delete_otp_codes_task():
    expired_time = datetime.now(tz=ZoneInfo("Asia/Tehran")) - timedelta(seconds=90)
    OtpCode.objects.filter(created__lt=expired_time).delete()
