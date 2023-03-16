from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistration(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите логин', 'class': 'form-control'})
    )

    email = forms.EmailField(
        label='Почта',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите почту', 'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Пароль повторно',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль повторно', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']