from zoneinfo import available_timezones
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from ..user_accounts.models import *
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def scheduleGroupSessions(request, username):

  user = User.objects.get(username=username)
 

  group_booking_form = GroupBookingForm()

  if request.method == 'POST': # if user sent info
    group_booking_form = GroupBookingForm(request.POST)
    if group_booking_form.is_valid():
      group_booking = group_booking_form.save(commit=False)
      group_booking.service_provider = request.user
      group_booking.save()

      return redirect('available-group-sessions', username)

  
  context = {'user':user, 
            'group_booking_form': group_booking_form,
           
            }

  return render(request, 'group_sessions/sp_schedule_group_sessions.html', context)


def updateGroupSession(request, pk):

  # user = User.objects.get(username=username)
  group_booking = GroupBooking.objects.get(id=pk)

  group_booking_form = GroupBookingForm(instance=group_booking)

  if request.method == 'POST': # if user sent info
    group_booking_form = GroupBookingForm(request.POST, instance=group_booking) ## populated with the data that the user sent - update a group, do not create a new one
    if group_booking_form.is_valid():
      group_booking.save()

      return redirect('available-group-sessions', group_booking.service_provider)

  
  context = {
            'group_booking_form': group_booking_form,
           
            }

  return render(request, 'group_sessions/sp_schedule_group_sessions.html', context)

def availableGroupSessions(request, username):

  user = User.objects.get(username=username)
  current_date = datetime.now().date()  
  current_time = datetime.now().time() 

  available_group_sessions = GroupBooking.objects.filter(service_provider=request.user)
  context = {'user':user,
            'current_date': current_date,
            'current_time': current_time,
            'available_group_sessions':available_group_sessions,
            }

  return render(request, 'group_sessions/sp_available_group_sessions.html', context)
  
def clientGroupSessions(request, username):

  user = User.objects.get(username=username)
  client = Client.objects.get(user=user.id)

  current_date = datetime.now().date()  
  current_time = datetime.now().time() 

  client_group_sessions = GroupBooking.objects.filter(members=request.user)
  context = {'user':user, 'client':client,
            'current_date': current_date,
            'current_time': current_time,
            'client_group_sessions':client_group_sessions,
            }



  return render(request, 'group_sessions/client_group_sessions.html', context)

  
def liveSessionsList(request):
  available_group_sessions = GroupBooking.objects.all()
  current_date = datetime.now().date()  
  current_time = datetime.now().time()  
 
  context = {'available_group_sessions': available_group_sessions,
            'current_date': current_date,
            'current_time': current_time,
            }
  return render(request, 'group_sessions/group_signup.html', context)



def groupSignUpConfirmation(request, pk):
  group_signup = GroupBooking.objects.get(id=pk) # get_object_or_404(GroupBooking, id=pk )

  if request.method == 'POST':
     group_signup.members.add(request.user)
     return redirect('client-group-sessions', request.user)
  
  context = {
    'group_signup':group_signup,
   }

  return render(request, 'group_sessions/group_signup_confirmation.html', context)


def clientLeaveGroup(request, pk):
  client_leave_group = GroupBooking.objects.get(id=pk) # get_object_or_404(GroupBooking, id=pk, )

  if request.method == 'POST': # if user sent info
      client_leave_group.members.remove(request.user)
      return redirect('client-group-sessions', request.user)

  context = {
    'client_leave_group': client_leave_group,
   
  }
  return render(request, 'group_sessions/client_leave_group.html', context)


 
 


def groupBookingCancellation(request, pk):
  group_booking = GroupBooking.objects.get(id=pk)

  group_cancellation_form = CancelGroupBookingForm(instance=group_booking)
  if request.method == 'POST': # if user sent info
    group_cancellation_form = CancelGroupBookingForm(request.POST, instance=group_booking)
    if group_cancellation_form.is_valid():
      sp_cancel = group_cancellation_form.save()
      sp_cancel.save()
      return redirect('available-group-sessions', group_booking.service_provider)
      
  context = {'group_booking': group_booking,
        
             ' group_cancellation_form':  group_cancellation_form,
             }
  return render(request, 'group_sessions/group_booking_cancellation.html', context)
  
