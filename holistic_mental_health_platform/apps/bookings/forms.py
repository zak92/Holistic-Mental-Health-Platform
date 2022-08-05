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

# service provider will use this form to schedule available bookings
class BookingForm(ModelForm):
  class Meta:
    model = Booking
    fields = ['date', 'time', 'duration']
    widgets = {
      'date': DatePickerInput(),
      'time':  TimePickerInput(),
    }

  def __init__(self,*args,**kwargs):
      super(BookingForm,self).__init__(*args,**kwargs)

      self.fields["date"].label="Date"
      self.fields["date"].widget=DatePickerInput(attrs={"class":"form-control", 
      "style": "margin-bottom:1.25em; background-color: #FFC3C3;color: white;border-radius: 1em;margin-left:1em; width: 40%"})

      self.fields["time"].label="Time"
      self.fields["time"].widget=TimePickerInput(attrs={"class":"form-control", 
       "style": "margin-bottom:1.25em; background-color: #FFC3C3;color: white;border-radius: 1em;margin-left:1em; width: 30%"})

      self.fields["duration"].label="Duration"
      self.fields["duration"].widget=forms.NumberInput(attrs={"class":"form-control", 
       "style": "width:30%;margin-bottom:1.25em; background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})
       
# clients will use this from to book appointments with service providers
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

# clients can cancel bookings
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

# service providers will confirm the booking made by the client
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

# service providers can cancel client bookings
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