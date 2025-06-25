from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

class Command(BaseCommand):
    help = 'Remove all expired Otp codes'
    def handle(self, *args, **options):
        expired_time = datetime.now(tz=ZoneInfo("Asia/Tehran")) - timedelta(seconds=90)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write(self.style.SUCCESS('All Otp codes removed.'))