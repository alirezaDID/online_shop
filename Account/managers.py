from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self ,email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user
    
    def create_seller(self, email, password):
        user = self.create_user(email, password)
        user.is_seller = True
        user.save()
        return user
