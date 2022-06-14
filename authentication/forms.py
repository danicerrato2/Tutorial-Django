from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(
        widget=forms.PasswordInput, help_text="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput, help_text="Confirm password")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",
            "email", "password1", "password2")