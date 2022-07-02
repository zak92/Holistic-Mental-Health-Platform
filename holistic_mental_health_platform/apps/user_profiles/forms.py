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

class UpdateClientProfileForm(ModelForm):
  class Meta:
    model = Client
    fields = ['bio', 'status']

class UpdateServiceProviderProfileForm(ModelForm):
  class Meta:
    model = ServiceProvider
    fields = ['about', 'announcements']