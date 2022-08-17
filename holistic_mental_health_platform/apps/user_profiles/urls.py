from re import template
from django.urls import path
from apps.user_profiles import views


from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path('client/<str:username>/', views.clientProfile, name='client-profile'),
    path('edit-client-profile/<str:username>/', views.updateClientProfile, name='edit-client-profile'),
    path('service-provider/<str:username>/', views.serviceProviderProfile, name='service-provider-profile'),
    path('edit-service-provider/<str:username>/', views.updateServiceProviderProfile, name='edit-service-provider-profile'),
    path('change-password', views.changePassword, name='change-password'),

]
  