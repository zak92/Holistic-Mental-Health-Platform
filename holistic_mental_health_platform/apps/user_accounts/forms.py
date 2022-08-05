from cProfile import label
from msilib.schema import CustomAction
from xmlrpc.client import Boolean
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from .models import *
from django.db import transaction
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField



class ClientUserCreationForm(UserCreationForm):
  email = forms.EmailField()
  agree = forms.BooleanField()
  
  class Meta(UserCreationForm.Meta):
    model = User
    fields = ['username' , 'email', 'password1', 'password2', 'agree']

  def __init__(self,*args,**kwargs):
      super(ClientUserCreationForm,self).__init__(*args,**kwargs)
      self.fields["username"].label=""
      self.fields["username"].widget=forms.TextInput(attrs={"placeholder": "Username","class":"form-control"})

      self.fields["email"].label=""
      self.fields["email"].widget=forms.TextInput(attrs={"placeholder": "Email","class":"form-control"})

      self.fields["password1"].label=""
      self.fields["password1"].widget=forms.PasswordInput(attrs={"placeholder": "Password", "class":"form-control"})

      self.fields["password2"].label=""
      self.fields["password2"].widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class":"form-control"})

      self.fields["agree"].label="I agree to the terms and conditions"
      self.fields["agree"].widget= forms.CheckboxInput(attrs={
        "style": "padding: 0; margin-left: 1em; text-align:center; width: 20px;" , 
        "class": 'form-control'
      })


  
    
  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.is_client = True
    user.save()
    client = Client.objects.create(user=user)
    client.client_agree_to_T_and_Cs = True
    client.save()
    return user

  def clean(self):
    '''https://simpleisbetterthancomplex.com/tutorial/2017/02/06/how-to-implement-case-insensitive-username.html'''
    cleaned_data = super(ClientUserCreationForm, self).clean()
    username = cleaned_data.get('username')
    if username and User.objects.filter(username__iexact=username).exists():
        self.add_error('username', 'A user with that username already exists.')
    return cleaned_data




class ServiceProviderRegistrationApplicationForm(ModelForm):
  
  country = CountryField(blank_label='Select your country').formfield(
        widget=CountrySelectWidget(
           attrs={
            "style": "background-color: #FFC3C3; border-radius:1em; margin-left:0.5em; width:100%",
            }
        )
    )
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'country', 'city']
 
  
  def __init__(self,*args,**kwargs):
    super(ServiceProviderRegistrationApplicationForm,self).__init__(*args,**kwargs)
    self.fields["first_name"].label=""
    self.fields["first_name"].widget=forms.TextInput(attrs={"placeholder": "First name","class":"form-control", "style": "margin-bottom:1.25em;"})

    self.fields["last_name"].label=""
    self.fields["last_name"].widget=forms.TextInput(attrs={"placeholder": "Last name","class":"form-control", "style": "margin-bottom:1.25em;"})

    self.fields["email"].label=""
    self.fields["email"].widget=forms.TextInput(attrs={"placeholder": "Email","class":"form-control",  "style": "margin-bottom:1.25em;"})

    self.fields["username"].label=""
    self.fields["username"].widget=forms.TextInput(attrs={"placeholder": "Username","class":"form-control"})

    self.fields["country"].label=""
   

    self.fields["city"].label=""
    self.fields["city"].widget=forms.TextInput(attrs={"placeholder": "Your city","class":"form-control"})

     
  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.is_service_provider = True  
    user.save() 
    service_provider = ServiceProvider.objects.create(user=user)
    service_provider.save()
    return user



