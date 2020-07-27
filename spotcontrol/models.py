from django.db import models
from django.conf import settings


# Create your models here.

class RecentCrews(models.Model):
    crew_id = models.UUIDField()
    crew_title = models.CharField(max_length=100, blank=True, null=True)
    last_active_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_active_date']

    def __str__(self):
        # return str(self.crew_title) + str(self.last_active_date)
        return f'{self.crew_id} ({self.crew_title}) - last active {self.last_active_date}'

class SpotifyUser(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=1000, blank=True, null=True)
    refresh_token = models.CharField(max_length=1000, blank=True, null=True)
    expires_in = models.DateTimeField()
    most_recent_device = models.CharField(max_length=1000, blank=True, null=True)
    most_recent_crews = models.ManyToManyField(RecentCrews)

    def __str__(self):
        return str(self.username)