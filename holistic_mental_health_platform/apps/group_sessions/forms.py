
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


class GroupBookingForm(ModelForm):
  category = forms.ModelChoiceField(queryset = Category.objects.all())
  class Meta:
    model = GroupBooking
    fields = ['group_name', 'description', 'category', 'date', 'time', 'duration', 'max_members']
    widgets = {
      'date': DatePickerInput(),
      'time':  TimePickerInput(),
    }
  def __init__(self,*args,**kwargs):
      super(GroupBookingForm,self).__init__(*args,**kwargs)

      self.fields["description"].label="Description"
      self.fields["description"].widget=forms.Textarea(attrs={"class":"form-control", 
        "style": "width:98%;height:150px;overflow-y: scroll;background-color: #FFC3C3;color: white;border-radius: 1em;margin-left:1em;"})

      self.fields["date"].label="Date"
      self.fields["date"].widget=DatePickerInput(attrs={"class":"form-control", 
      "style": "width:50%;margin-bottom:1.25em; background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})

      self.fields["time"].label="Time"
      self.fields["time"].widget=TimePickerInput(attrs={"class":"form-control", 
       "style": "width:40%;margin-bottom:1.25em; background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})

      self.fields["duration"].label="Duration"
      self.fields["duration"].widget=forms.NumberInput(attrs={"class":"form-control", 
       "style": "width:30%;margin-bottom:1.25em; background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})

      self.fields["max_members"].label="Maximum members"
      self.fields["max_members"].widget=forms.NumberInput(attrs={"class":"form-control", 
       "style": "width:30%;margin-bottom:1.25em; background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})


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