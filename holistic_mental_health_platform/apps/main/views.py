from django.shortcuts import render


from django.shortcuts import render, redirect
from .models import *
from ..user_accounts.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
 context = {'title': 'HOME'}
 return render(request, 'main/home.html', context)
