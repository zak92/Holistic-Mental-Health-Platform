from re import template
from django.urls import path
from apps.user_profiles import views


from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path('client/<str:username>/', views.clientProfile, name='client-profile'),
    path('service-provider/<str:username>/', views.serviceProviderProfile, name='service-provider-profile'),
 
   

]
  