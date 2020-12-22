from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['university', 'field', 'entrance_year', 'phone_number']


class NamesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

