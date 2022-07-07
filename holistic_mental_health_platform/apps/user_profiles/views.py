from http import client
from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import *
from .forms import *
from ..user_accounts.models import *
from ..bookings.models import *
from ..group_sessions.models import *
from django.contrib.auth.decorators import login_required
from apps.user_profiles import views
from django.urls import reverse
import datetime
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.

#---------------------------client profile page ----------------------------
def clientProfile(request, username):
  # get user object
  user = User.objects.get(username=username)
  # get client object with user id
  client = Client.objects.get(user=user.id)
  context = { 'user':user, 'client':client }
  return render(request, 'user_profiles/client_profile.html', context)

#-------------------service provider profile page----------------------------
def serviceProviderProfile(request, username):
  # get user object
  user = User.objects.get(username=username)
  # get service_provider object with user id
  service_provider = ServiceProvider.objects.get(user=user.id)
  context = {'user':user, 'service_provider': service_provider }
  return render(request, 'user_profiles/service_provider_profile.html', context)

#------------------- update client profile page-------------------------------
def updateClientProfile(request, username):
  user = User.objects.get(username=username)
  client = Client.objects.get(user=user.id)

  update_user_profile_form = UpdateUserProfileForm(instance=request.user)
  update_client_profile_form = UpdateClientProfileForm(instance=client)
  if request.method == 'POST': # if user sent info
    # populated with the data that the user sent - update a profile, do not create a new one
    update_user_profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user)  
    update_client_profile_form = UpdateClientProfileForm(request.POST, instance=client)
    if update_user_profile_form.is_valid() and update_client_profile_form.is_valid(): # validate the data
      update_user_profile_form.save()
      update_client_profile_form.save()
      return redirect('client-profile', request.user)

  context = {
              'update_client_profile_form': update_client_profile_form,
              'update_user_profile_form': update_user_profile_form
            
            }

  return render(request, 'user_profiles/edit_client_profile.html', context)



#-------------------update service provider profile page----------------------------
def updateServiceProviderProfile(request, username):
  user = User.objects.get(username=username)
  service_provider = ServiceProvider.objects.get(user=user.id)

  update_user_profile_form = UpdateUserProfileForm(instance=request.user)
  update_service_provider_profile_form = UpdateServiceProviderProfileForm(instance=service_provider)
  if request.method == 'POST': # if user sent info
    # populated with the data that the user sent - update a profile, do not create a new one
    update_user_profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user)  
    update_service_provider_profile_form = UpdateServiceProviderProfileForm(request.POST, instance=service_provider)
    if update_user_profile_form.is_valid() and update_service_provider_profile_form.is_valid(): # validate the data
      update_user_profile_form.save()
      update_service_provider_profile_form.save()
      return redirect('service-provider-profile', request.user)
  context = {
              'update_user_profile_form':update_user_profile_form,
              'update_service_provider_profile_form': update_service_provider_profile_form
            }

  return render(request, 'user_profiles/edit_service_provider_profile.html', context)


#--------------------------------change password page-------------------------------
def changePassword(request):
  password_change_form = PasswordChangeForm(user=request.user)

  if request.method == 'POST':
    password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
    if password_change_form.is_valid():
      password_change_form.save()
      # remain logged in after password has changed
      update_session_auth_hash(request, password_change_form.user) 
      return redirect('home')
      
    
  context = {'password_change_form': password_change_form}

  return render(request, 'user_profiles/password_change.html', context)

