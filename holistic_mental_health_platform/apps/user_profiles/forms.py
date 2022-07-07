from msilib.schema import CustomAction
from xmlrpc.client import Boolean
from django import forms
from django.forms import DateInput, ModelForm

from .models import *
from ..user_accounts.models import *
from django.db import transaction



class UpdateUserProfileForm(ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'country', 'city', 'profile_picture']

  # def clean(self):
  #   '''https://simpleisbetterthancomplex.com/tutorial/2017/02/06/how-to-implement-case-insensitive-username.html'''
  #   cleaned_data = super(UpdateClientProfileForm, self).clean()
  #   username = cleaned_data.get('username')
  #   if username and User.objects.filter(username__iexact=username).exists():
  #       self.add_error('username', 'A user with that username already exists.')
  #   return cleaned_data

class UpdateClientProfileForm(ModelForm):
  class Meta:
    model = Client
    fields = ['bio', 'status']

class UpdateServiceProviderProfileForm(ModelForm):
  class Meta:
    model = ServiceProvider
    fields = ['about', 'announcements']