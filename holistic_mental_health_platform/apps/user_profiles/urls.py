from re import template
from django.urls import path
from apps.user_profiles import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('client', views.clientProfile, name='client-profile'),
    path('service-provider', views.serviceProviderProfile, name='service-provider-profile'),
  
   

]
  