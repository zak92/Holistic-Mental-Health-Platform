from re import template
from django.urls import path
from apps.users import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('registration/client', views.clientsRegistration, name='registration'),
    path('application/service-provider', views.serviceProviderApplication, name='application'),
    path('login/client', views.clientsLogin, name='login'),
    path('login/service-provider', views.serviceProviderLogin, name='sp-login'), 
    path('logout/client', views.clientsLogout, name='logout'),
    path('', views.home, name='home'), 
    # class based views - login/logout
    # https://www.youtube.com/watch?v=3aVqWaLjqS4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=7
    
    
]