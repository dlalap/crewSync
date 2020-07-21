from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(label='email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
    ))
