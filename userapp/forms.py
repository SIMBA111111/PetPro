from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ["username", "password", ]


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(label='', max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # username = forms.CharField(label="имя пользователя", widget=forms.TextInput())
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля '}))

    class Meta:
        model = User
        fields = [
            # "username",
            # "email",
            # "password",
        ]
