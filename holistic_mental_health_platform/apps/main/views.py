from django.shortcuts import render


from django.shortcuts import render, redirect
from .models import *
from ..user_accounts.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
 context = {'title': 'HOME',
              }
 return render(request, 'main/home.html', context)

def serviceProviderList(request):
  service_providers = User.objects.filter(is_service_provider=1)
  context = {'title': 'Service Providers', 'service_providers': service_providers}
  return render(request, 'main/service_provider_list.html', context)
