from re import template
from django.urls import path
from apps.user_accounts import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('registration/client', views.clientsRegistration, name='registration'),
    path('application/service-provider', views.serviceProviderApplication, name='application'),
    path('login', views.userLogin, name='login'),
    path('logout', views.userLogout, name='logout'),
    #path('forgot-password', views.forgotPassword, name='forgot-password'),

    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='user_accounts/password_reset.html'), 
         name='reset_password'),

    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name='user_accounts/password_reset_sent.html'), 
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='user_accounts/password_reset_form.html'), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='user_accounts/password_reset_done.html'), 
         name="password_reset_complete"),
    
    
    
    
]
# password reset
# uidb64 - the user's id encoded on base 64
# token - token to check that the password is valid

# http://127.0.0.1:8080/accounts/reset_password
# http://127.0.0.1:8080/accounts/reset_password_sent
# http://127.0.0.1:8080/accounts/reset_password_complete
