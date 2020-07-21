from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

appname = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # path('login/', views.login_request, name='login'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout/', views.logout_request, name='logout')
]