
from django import forms
from django.forms import DateInput, ModelForm

from .models import *

from django.db import transaction




from django.db.models import F

class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'

    
choices = [('Fitness', 'Fitness'), 
           ('Meditation', 'Meditation'), 
           ('Yoga', 'Yoga'), 
           ('Nutrition', 'Nutrition'), 
           ('Counselling and advice', 'Counselling and advice')
           ]
class GroupBookingForm(ModelForm):
  class Meta:
    model = GroupBooking
    fields = ['group_name', 'description', 'category', 'date', 'time', 'duration', 'max_members']
    widgets = {
      'date': DatePickerInput(),
      'time':  TimePickerInput(),
      'category': forms.Select(choices=choices, attrs={'class':'form-control'})
    }


class CancelGroupBookingForm(ModelForm):
  
  class Meta:
    model = GroupBooking
    fields = ['cancelled']
    widgets = {'cancelled': forms.HiddenInput()}

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.cancelled = True  
    user.save() 
    return user