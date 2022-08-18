from django import forms
from django.contrib.auth.forms import UserCreationForm
from donadona.models import User


class UserForm(UserCreationForm):
    username = forms.CharField(label="ID")
    nickname = forms.CharField(label="이름")
    phone = forms.CharField(label="전화번호")

    class Meta:
        model = User
        fields = ("username", "nickname", "email", "phone", "alarm")
