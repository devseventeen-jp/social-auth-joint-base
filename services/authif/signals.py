from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# class AuthConfig(AppConfig):
#    default_auto_field = "django.db.models.BigAutoField"
#     name = "authif"
# 
#     def ready(self):
#         import authif.signals
