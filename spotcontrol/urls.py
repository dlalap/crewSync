from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('spot_connect/', views.connect_spotify, name='connect_spotify'),
    path('redir_uri/', views.auth_spotify, name='auth_spotify'),
    path('spot_refresh/', views.refresh_spotify, name='refresh_spotify'),
    path('log_playback_device/', views.log_playback_device, name='log_playback_device'),
    path('spot_auth_result/<authresult>', views.AuthResult.as_view(), name='spot_auth_result'),
    path('control/', views.Index.as_view(), name='control'),
    path('control/<str:crew_id>/', views.room, name='room'),
    path('testendpoint/', views.test, name='test'),
    path('get_auth_token/', views.get_auth_token, name='get_auth_token')
]