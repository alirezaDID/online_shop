from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_staff(self):
        return self.is_admin

class Profile(models.Model):
	# relational fields
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile')
	
	# info fields
	first_name = models.CharField(max_length=250, blank=True, null=True)
	last_name = models.CharField(max_length=250, blank=True, null=True)
	image = models.ImageField(upload_to='profiles/', default='profiles/defualt.jpg')


	def __str__(self):
		return self.full_name if self.first_name and self.last_name else self.user.__str__() 

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"
	

class Shop(models.Model):
	# relation fields
	seller = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='shop')

	# info fields
	name = models.CharField(max_length=250)
	address = models.CharField(max_length=400, blank=True, null=True)
	cell_phone = models.CharField(max_length=11)

	def __str__(self):
		return self.name if self.name else self.seller.__str__()


class OtpCode(models.Model):
    email = models.EmailField(unique=True, null=True)
    code = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    code_time = models.DateTimeField(default=(timezone.now() + timedelta(minutes=2)))


    def is_expire(self):
          return True if timezone.now() >= self.code_time else False 
    
    @property
    def expire_time(self):
          return self.code_time - timezone.now()