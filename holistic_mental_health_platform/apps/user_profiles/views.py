from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import *
from .forms import *
from ..users.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/client')
def clientProfile(request):

  context = {}
  return render(request, 'user_profiles/client_profile.html', context)


@login_required(login_url='/accounts/login/client')
def clientProfile(request):

  context = {}
  return render(request, 'user_profiles/client_profile.html', context)
