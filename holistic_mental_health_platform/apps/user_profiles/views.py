from http import client
from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import *
from .forms import *
from ..user_accounts.models import *
from ..bookings.models import *
from django.contrib.auth.decorators import login_required
from apps.user_profiles import views

import datetime
from datetime import datetime

# Create your views here.
# @login_required(login_url='/accounts/login/client')  UNCOMMENT LATER
def clientProfile(request, username):
   # get user object
  user = User.objects.get(username=username)
  client = Client.objects.get(user=user.id)

  current_date = datetime.now().date()  
  current_time = datetime.now().time()  
  my_bookings = Booking.objects.filter(client=request.user)
  context = {'user':user, 'client':client,
            'current_date': current_date,
            'current_time': current_time,
            'my_bookings': my_bookings,
            }


  return render(request, 'user_profiles/client_profile.html', context)


# @login_required(login_url='/accounts/login/service-provider')
def serviceProviderProfile(request, username):
  user = User.objects.get(username=username)
  form = BookingForm()
  
  current_date = datetime.now().date()  
  current_time = datetime.now().time()  

  if request.method == 'POST': # if user sent info
    form = BookingForm(request.POST)
    if form.is_valid():
      booking = form.save(commit=False)
      booking.service_provider = request.user
      booking.save()

      return redirect('service-provider-profile', username)

  available_bookings = Booking.objects.filter(service_provider=request.user)


     
  context = {'user':user, 
            'form':form,
            'available_bookings': available_bookings,
            'current_date': current_date,
            'current_time': current_time,
            }

  return render(request, 'user_profiles/service_provider_profile.html', context)



  
  

  


