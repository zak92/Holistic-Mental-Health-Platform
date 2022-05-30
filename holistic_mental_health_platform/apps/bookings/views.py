
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from ..user_accounts.models import *
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime

# Create your views here.

def individualBooking(request, username):
  user = User.objects.get(username=username) # get user 
  available_bookings = Booking.objects.filter(service_provider=user)
  current_date = datetime.now().date()  
  current_time = datetime.now().time()  
  context = {'available_bookings': available_bookings, 
            'user': user, 
            'current_date': current_date,
            'current_time': current_time,
            }
  return render(request, 'bookings/booking_individual.html', context)

def bookingConfirmation(request, pk):
  
  booking = Booking.objects.get(id=pk)

  booking_form = ClientBookingForm(instance=booking)
  if request.method == 'POST': # if user sent info
    booking_form = ClientBookingForm(request.POST, instance=booking)
    if booking_form.is_valid():
      book = booking_form.save()
      book.client = request.user
      book.save()
      return redirect('client-profile', booking.client)
  


  context = {'booking': booking,
             'booking_form': booking_form, 
             
             }
  return render(request, 'bookings/booking_confirmation.html', context)

def bookingConfirmationSP(request, pk):
  
  booking = Booking.objects.get(id=pk)


  service_provider_booking_form = ConfirmBookingForm(instance=booking)
  if request.method == 'POST': # if user sent info
    service_provider_booking_form = ConfirmBookingForm(request.POST, instance=booking)
    if service_provider_booking_form.is_valid():
      sp_book = service_provider_booking_form.save()
      sp_book.save()
      return redirect('service-provider-profile', booking.service_provider)
      
  context = {'booking': booking,
        
             'service_provider_booking_form':  service_provider_booking_form
             }
  return render(request, 'bookings/service_provider_booking_confirmation.html', context)

def bookingCancellationSP(request, pk):
  booking = Booking.objects.get(id=pk)


  sp_booking_form = CancelBookingForm(instance=booking)
  if request.method == 'POST': # if user sent info
    sp_booking_form = CancelBookingForm(request.POST, instance=booking)
    if sp_booking_form.is_valid():
      sp_book = sp_booking_form.save()
      sp_book.save()
      return redirect('service-provider-profile', booking.service_provider)
      
  context = {'booking': booking,
        
             'sp_booking_form':  sp_booking_form
             }
  return render(request, 'bookings/service_provider_cancel_booking.html', context)


def bookingCancellation(request, pk):
  booking = Booking.objects.get(id=pk)


  client_booking_form = ClientCancelBookingForm(instance=booking)
  if request.method == 'POST': # if user sent info
    client_booking_form = ClientCancelBookingForm(request.POST, instance=booking)
    if client_booking_form.is_valid():
      client_book = client_booking_form.save()
      client_book.save()
      return redirect('client-profile', booking.client)
      
  context = {'booking': booking,
        
             'sp_booking_form':  client_booking_form
             }
  return render(request, 'bookings/booking_cancellation.html', context)