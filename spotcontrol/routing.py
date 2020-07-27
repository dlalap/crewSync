from django.urls import re_path
# from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/spotcontrol/(?P<room_name>\w+)/$', consumers.SpotifyConsumer),
]

# websocket_urlpatterns = [
#     url(r'ws/spotcontrol/(?P<room_name>\w+)/$', consumers.SpotifyConsumer)
# ]