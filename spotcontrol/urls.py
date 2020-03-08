from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('redir_uri/', views.auth_spotify, name='auth_spotify'),
    path('control/', views.index, name='index'),
    path('control/<str:room_name>/', views.room, name='room'),
]