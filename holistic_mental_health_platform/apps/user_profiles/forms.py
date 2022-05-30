from msilib.schema import CustomAction
from xmlrpc.client import Boolean
from django import forms
from django.forms import DateInput, ModelForm

from .models import *
from ..bookings.models import *
from django.db import transaction



# class BookingForm(forms.Form):
#   date_input = forms.DateField(widget=AdminDateWidget())
#   time_input = forms.DateField(widget=AdminTimeWidget())

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




