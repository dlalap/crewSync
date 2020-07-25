from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('spot_connect/', views.connect_spotify, name='connect_spotify'),
    path('redir_uri/', views.auth_spotify, name='auth_spotify'),
    path('spot_refresh/', views.refresh_spotify, name='refresh_spotify'),
    path('spot_auth_result/<authresult>', views.AuthResult.as_view(), name='spot_auth_result'),
    path('control/', views.index, name='index'),
    path('control/<str:room_name>/', views.room, name='room'),
]