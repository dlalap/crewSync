from django.db import models
from django.conf import settings


# Create your models here.
class SpotifyUser(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
