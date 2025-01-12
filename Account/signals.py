from django.db.models.signals import post_save  
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=CustomUser)  
def profile_creator(sender, instance, created, **kwargs):  
    if created:
        profile = Profile.objects.create(user=instance)
        if instance.is_seller:
            Shop.objects.create(seller=profile)
            profile.image = 'profiles/default_seller.jpg'
        profile.save()

        