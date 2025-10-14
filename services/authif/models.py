from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    is_approved = models.BooleanField(default=False)   # for approval control
    '''
    other profile.
    '''
 #   display_name = models.CharField(max_length=100, blank=True)
 #   company_name = models.CharField(max_length=200, blank=True) 
 #   phone_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"
