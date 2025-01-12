from kavenegar import *
from django.core.mail import send_mail
from django.conf import settings
import threading
from django.core.exceptions import ValidationError  
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _

def send_code(email, code):
    subject = ''
    message = f'کد احراز هویت شما در سایت : {code}'
    recipient_list = [email] 
    fail_silently = True

    # send code without delay with threading
    send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject=subject,
        message=message,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        
    )

class PasswordValidation:
    def __init__(self, password1, password2):
        self.passsword1 = password1
        self.passsword2 = password2

    def same_password_validation(self):
        if self.passsword1 != self.passsword2:
            raise ValidationError(_("passwords doesn't match!"))
    
    def strong_validation(self):
        password_validation.validate_password(self.passsword1)

    def validation(self):
        self.same_password_validation()
        self.validation()
        