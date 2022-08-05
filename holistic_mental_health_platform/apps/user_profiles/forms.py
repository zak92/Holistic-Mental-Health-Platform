from msilib.schema import CustomAction
from tkinter.ttk import Style
from xmlrpc.client import Boolean
from django import forms
from django.forms import DateInput, ModelForm

from .models import *
from ..user_accounts.models import *
from django.db import transaction
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from django.contrib.auth.forms import PasswordChangeForm
from ckeditor.widgets import CKEditorWidget



class UpdateUserProfileForm(ModelForm):
  country = CountryField(blank_label='Select your country').formfield(
        widget=CountrySelectWidget(
           attrs={
            "style": "background-color: #FFC3C3; border-radius:1em; margin-left:0.5em; width:100%",
            }
        )
    )
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'country', 'city', 'profile_picture']

  def __init__(self,*args,**kwargs):
    super(UpdateUserProfileForm,self).__init__(*args,**kwargs)

    self.fields["first_name"].label="First name"
    self.fields["first_name"].widget=forms.TextInput(attrs={"placeholder": "First name","class":"form-control", "style": "margin-bottom:1.25em;"})

    self.fields["last_name"].label="Last name"
    self.fields["last_name"].widget=forms.TextInput(attrs={"placeholder": "Last name","class":"form-control", "style": "margin-bottom:1.25em;"})

    self.fields["username"].label="Username"
    self.fields["username"].widget=forms.TextInput(attrs={"placeholder": "Username","class":"form-control"})

    self.fields["email"].label="Email"
    self.fields["email"].widget=forms.TextInput(attrs={"placeholder": "Email","class":"form-control"})

    self.fields["city"].label="City"
    self.fields["city"].widget=forms.TextInput(attrs={"placeholder": "Your city","class":"form-control"})

    self.fields["profile_picture"].label="Change profile picture"
    self.fields["profile_picture"].widget=forms.FileInput(attrs={"class":"form-control",
    "style": "background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})

   

class UpdateClientProfileForm(ModelForm):


  class Meta:
    model = Client
    fields = ['bio', 'status']

  def __init__(self,*args,**kwargs):
    super(UpdateClientProfileForm,self).__init__(*args,**kwargs)

    self.fields["status"].label="Status"
    self.fields["status"].widget=forms.Textarea(attrs={"placeholder": "Status","class":"form-control", 
    "style": "width:98%;height:90px;overflow-y: scroll;background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})

    self.fields["bio"].label="Bio"
    self.fields["bio"].widget=forms.Textarea(attrs={"placeholder": "Bio","class":"form-control", 
    "style": "width:98%;height:150px;overflow-y: scroll;background-color: #FFC3C3;color: white;border-radius: 1em;margin-left:1em;"})

class UpdateServiceProviderProfileForm(ModelForm):
  about = forms.CharField(widget=CKEditorWidget(
    attrs={
            "style": "background-color: #FFC3C3; border-radius:1em; margin-left:0.5em; width:100%",
          }
  ))
  class Meta:
    model = ServiceProvider
    fields = ['announcements', 'about']

  def __init__(self,*args,**kwargs):
    super(UpdateServiceProviderProfileForm,self).__init__(*args,**kwargs)

    #self.fields["about"].label="About"
    # self.fields["about"].widget=forms.TextInput(attrs={"placeholder": "About","class":"form-control"})

    self.fields["announcements"].label="Announcements"
    self.fields["announcements"].widget=forms.Textarea(attrs={"placeholder": "Announcements","class":"form-control",
     "style": "width:98%;height:90px;overflow-y: scroll;background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})


class UserPasswordChangeForm(PasswordChangeForm):
  class Meta:
    model = User
    fields = '__all__'

  def __init__(self,*args,**kwargs):
    super(UserPasswordChangeForm,self).__init__(*args,**kwargs)

    self.fields["old_password"].label=""
    self.fields["old_password"].widget=forms.PasswordInput(attrs={"placeholder": "Old Password", "class":"form-control"})

    self.fields["new_password1"].label=""
    self.fields["new_password1"].widget=forms.PasswordInput(attrs={"placeholder": "New Password", "class":"form-control"})
  
    self.fields["new_password2"].label=""
    self.fields["new_password2"].widget=forms.PasswordInput(attrs={"placeholder": "Confirm New Password", "class":"form-control"})
  
  