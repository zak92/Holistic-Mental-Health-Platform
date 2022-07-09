from zoneinfo import available_timezones
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from ..user_accounts.models import *
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def scheduleGroupSessions(request, username):

  user = User.objects.get(username=username)
 

  group_booking_form = GroupBookingForm(initial = {'category': 1 })

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

@login_required(login_url='/accounts/login')
def availableGroupSessions(request, username):

  user = User.objects.get(username=username)
  if request.user != user:
    return redirect('home')
  current_date = datetime.now().date()  
  current_time = datetime.now().time() 

  available_group_sessions = GroupBooking.objects.filter(service_provider=user)
  context = {'user':user,
            'current_date': current_date,
            'current_time': current_time,
            'available_group_sessions':available_group_sessions,
            }

  return render(request, 'group_sessions/sp_available_group_sessions.html', context)

@login_required(login_url='/accounts/login')
def clientGroupSessions(request, username):

  user = User.objects.get(username=username)
  client = Client.objects.get(user=user.id)
  if request.user != user:
    return redirect('home')
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
  categories = Category.objects.all() 
  available_group_sessions = GroupBooking.objects.all()
  current_date = datetime.now().date()  
  current_time = datetime.now().time()  
 
  context = {'available_group_sessions': available_group_sessions,
            'current_date': current_date,
            'current_time': current_time,
            'categories': categories
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

@login_required(login_url='/accounts/login')
def clientLeaveGroup(request, pk):
  client_leave_group = GroupBooking.objects.get(id=pk) # get_object_or_404(GroupBooking, id=pk, )
  try:
    # returns a queryset
    client = client_leave_group.members.all().filter(username=request.user.username)[0:1].get()
    client_id = client.id
    user = User.objects.get(id=client_id)
  except ObjectDoesNotExist: # if user is not current user
    return redirect('home')
  

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


# category search
def searchByCategory(request, slug):
  # get post with unique slug
  categories = Category.objects.all() 
  category = get_object_or_404(Category, slug=slug)

  available_group_sessions = GroupBooking.objects.filter(category=category)

  current_date = datetime.now().date()  
  current_time = datetime.now().time()

  context = {
    'categories': categories,
    'category': category,
    'current_date': current_date,
    'current_time': current_time,
    'available_group_sessions': available_group_sessions
  }
  return render(request, 'group_sessions/category_search_results.html', context)

# text search
def searchByText(request):
  current_date = datetime.now().date()  
  current_time = datetime.now().time()
  categories = Category.objects.all()
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  # Search for groups
  available_group_sessions = GroupBooking.objects.filter(
     Q(group_name__icontains=q) |                                                                              
     Q(description__icontains=q)
    ) 
  
  context = {
    'current_date': current_date,
    'current_time': current_time,
    'available_group_sessions': available_group_sessions,
    'categories': categories,

  }
  return render(request, 'group_sessions/text_search_results.html', context)




