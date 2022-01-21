# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Employee
        fields = ['username', 'job_position', 'is_manager', 'company', 'phone_number']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = ['username', 'job_position', 'is_manager', 'company', 'phone_number']


class BirthdayForm(forms.Form):
    date = forms.DateField()
    number = forms.IntegerField()
