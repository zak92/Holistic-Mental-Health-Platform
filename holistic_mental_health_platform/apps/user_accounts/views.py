from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from apps.user_profiles import views

from apps.main import views
# Create your views here.
# https://www.youtube.com/watch?v=bTFRbAuU5Uo##############################



def clientsRegistration(request):

  client_registration_form = ClientUserCreationForm()

   # if this is a POST request we need to process the form data
  if request.method == 'POST':
    client_registration_form = ClientUserCreationForm(request.POST)

    if client_registration_form.is_valid():
      user = client_registration_form.save()
      username = client_registration_form.cleaned_data.get('username')
      
      user.username = user.username.lower() # username must be in lowercase
      user.save()

      messages.success(request, 'Account was created for ' + username)
      login(request, user) # log user in immediately
      messages.success(request, 'You are now  logged in as' + username)
      current_user = request.user
      
      return redirect('home')
  
      
  context = {'client_registration_form': client_registration_form }
  return render(request, 'user_accounts/clients_registration.html', context)

# https://www.youtube.com/watch?v=3aVqWaLjqS4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=7
def userLogin(request):
  current_user = request.user
  if request.user.is_authenticated:  # cant go to login page
    return redirect('home')
    #return redirect('client-profile', pk=current_user.id)
  if request.method == 'POST': # if user sent info
    username = request.POST.get('username').lower()  # populated with the data that the user sent
    password = request.POST.get('password')


   
    user = authenticate(request, username=username, password=password)
    current_user = request.user
    if user is not None:
      login(request, user)
      messages.success(request, 'You are successfully logged in as' + username)
      return redirect('home')
      #return redirect('client-profile', pk=current_user.id) 
    else:
      messages.info(request, 'Username or password is incorrect')
  

  
  context = {}
  return render(request, 'user_accounts/login.html', context)

def userLogout(request):
	logout(request)
	return redirect('login')

# https://stackoverflow.com/questions/27968417/django-form-with-fields-from-two-different-models
def serviceProviderApplication(request):
  service_provider_application_form = ServiceProviderRegistrationApplicationForm()
 
  if request.method == 'POST': # if user sent info
    service_provider_application_form = ServiceProviderRegistrationApplicationForm(request.POST)
  

    if service_provider_application_form.is_valid():
      user = service_provider_application_form.save()
      username = service_provider_application_form.cleaned_data.get('username')
      user.username = user.username.lower() # username must be in lowercase
      user.save()

     
      messages.success(request, 'Application Form Sent!')
      return redirect('home')

  context = {'service_provider_application_form': service_provider_application_form
            
            }
  return render(request, 'user_accounts/service_providers_registration_application.html', context)



