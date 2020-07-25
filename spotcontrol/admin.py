from django.contrib import admin
from .models import SpotifyUser


# Register your models here.
class SpotifyUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(SpotifyUser, SpotifyUserAdmin)