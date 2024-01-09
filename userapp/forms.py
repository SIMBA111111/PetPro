from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", ]


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="имя пользователя", widget=forms.TextInput())
    password1 = forms.CharField(label="пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="пароль повтор", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            # "password",
        ]