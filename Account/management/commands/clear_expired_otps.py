from django.core.management.base import BaseCommand
from Account.models import OtpCode
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "this command clear the all expired otps!"

    def add_arguments(self, parser): 
        parser.add_argument('-c', '--count', type=int, help='specify the count of otp count deletion proccess ') 
  

    def handle(self, *args, **kwargs):
        c = kwargs['count'] 
        expired_time = timezone.now() - timedelta(minutes=2)
        otp_obj_pks = OtpCode.objects.filter(created_on__lt=expired_time).values_list('pk', flat=True)

        if c:
            otp_obj_pks = otp_obj_pks[:c]

        exipred_otps = OtpCode.objects.filter(pk__in=otp_obj_pks)
        otp_count = exipred_otps.count()
        exipred_otps.delete()   

        self.stdout.write(
                self.style.SUCCESS(f"{otp_count} expired otps was deleted!")
            )
                
