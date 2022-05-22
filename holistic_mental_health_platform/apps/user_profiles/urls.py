from re import template
from django.urls import path
from apps.users import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('client', views.clientProfile, name='client-profile'),
    path('service_provider', views.ServiceProviderProfile, name='service-provider-profile'),
   

]