
from django.urls import path
from apps.bookings import views

urlpatterns = [
   
    path('booking-client/<str:username>/', views.individualBooking, name='client-booking'),
    path('confirm-booking/<str:pk>/', views.bookingConfirmationByClient, name='confirm-booking'), 
     path('cancel-booking/<str:pk>/', views.bookingCancellationByClient, name='cancel-booking'), 
     
    path('confirm-booking-sp/<str:pk>/', views.bookingConfirmationBySP, name='confirm-booking-sp'),
    path('cancel-booking-sp/<str:pk>/', views.bookingCancellationBySP, name='cancel-booking-sp'),    
   
    path('client/my-appointments/<str:username>/', views.clientAppointments, name='client-appointments'),#show client appointments

    path('service-provider/schedule-appointments/<str:username>/', views.serviceProviderScheduleAppointments, name='schedule-appointments'), 
    path('service-provider/booked/<str:username>/', views.serviceProviderBookedAppointments, name='booked-appointments'),   

]
  