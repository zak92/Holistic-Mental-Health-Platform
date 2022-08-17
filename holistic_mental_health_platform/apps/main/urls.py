from re import template
from django.urls import path
from apps.main import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.home, name='home'), 
   path('service-provider-list', views.serviceProviderList, name='service-provider-list'), 
    
]
  