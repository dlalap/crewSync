from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/spotcontrol/(?P<room_name>\w+)/$', consumers.SpotifyConsumer),
]