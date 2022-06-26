from msilib.schema import CustomAction
from xmlrpc.client import Boolean
from django import forms
from django.forms import DateInput, ModelForm

from .models import *

from django.db import transaction

class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'

class BookingForm(ModelForm):
  class Meta:
    model = Booking
    fields = ['date', 'time']
    widgets = {
      'date': DatePickerInput(),
      'time':  TimePickerInput(),
    }

class ClientBookingForm(ModelForm):
  
  class Meta:
    model = Booking
    fields = ['booked']
    widgets = {'booked': forms.HiddenInput()}

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.booked = True  
    user.cancelled = False
    user.save() 
    return user

class ClientCancelBookingForm(ModelForm):
  
  class Meta:
    model = Booking
    fields = ['cancelled']
    widgets = {'cancelled': forms.HiddenInput()}

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.booked = False
    user.cancelled = True  
    user.confirmed = False 
    user.save() 
    return user

class ConfirmBookingForm(ModelForm):
  
  class Meta:
    model = Booking
    fields = ['confirmed']
    widgets = {'confirmed': forms.HiddenInput()}

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.confirmed = True  
    user.save() 
    return user

class CancelBookingForm(ModelForm):
  
  class Meta:
    model = Booking
    fields = ['cancelled']
    widgets = {'cancelled': forms.HiddenInput()}

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.cancelled = True  
    user.confirmed = False 
    user.booked = False 
    user.save() 
    return user