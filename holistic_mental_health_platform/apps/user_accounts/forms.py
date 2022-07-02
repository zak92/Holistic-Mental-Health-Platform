from msilib.schema import CustomAction
from xmlrpc.client import Boolean
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from .models import *
from django.db import transaction

# styling forms - https://medium.com/swlh/how-to-style-your-django-forms-7e8463aae4fa
class ClientUserCreationForm(UserCreationForm):
  email = forms.EmailField()
  agree = forms.BooleanField()
  
  class Meta(UserCreationForm.Meta):
    model = User
    fields = ['username' , 'email', 'password1', 'password2', 'agree']

  def __init__(self,*args,**kwargs):
      super(ClientUserCreationForm,self).__init__(*args,**kwargs)
      self.fields["username"].label="Your Username"
      self.fields["username"].widget=forms.TextInput(attrs={"class":"form-control"})

      self.fields["email"].label="Your Email"
      self.fields["email"].widget=forms.TextInput(attrs={"class":"form-control"})

      self.fields["password1"].label="Your Password"
      self.fields["password1"].widget=forms.PasswordInput(attrs={"class":"form-control"})

      self.fields["password2"].label="Confirm Your Password"
      self.fields["password2"].widget=forms.PasswordInput(attrs={"class":"form-control"})

      self.fields["agree"].label="I agree to the Terms and Conditions"
      self.fields["agree"].widget= forms.CheckboxInput(attrs={'class': 'form-control'})


  
    
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
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'country', 'city']

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.is_service_provider = True  
    user.save() 
    service_provider = ServiceProvider.objects.create(user=user)
    service_provider.save()
    return user



