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

# Create your views here.
# @login_required(login_url='/accounts/login/client')  UNCOMMENT LATER
def clientProfile(request, username):
   # get user object
  user = User.objects.get(username=username)
  client = Client.objects.get(user=user.id)

  context = {'user':user, 'client':client,
            
            }


  return render(request, 'user_profiles/client_profile.html', context)



# @login_required(login_url='/accounts/login/service-provider')
def serviceProviderProfile(request, username):
  user = User.objects.get(username=username)
  context = {'user':user, 
           
           
            }

  return render(request, 'user_profiles/service_provider_profile.html', context)



