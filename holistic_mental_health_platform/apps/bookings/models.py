from pyexpat import model
from django.db import models
from django.forms import DateField

from ..user_accounts.models import *

# Create your models here.

class Booking(models.Model):
  service_provider = models.ForeignKey(User, related_name="service_provider", on_delete=models.CASCADE, null=True)
  date = models.DateField(null=True)
  time = models.TimeField(null=True)
  client = models.ForeignKey(User, related_name="client_booked", on_delete=models.CASCADE, null=True, blank=True)
  booked = models.BooleanField(default=False)
  confirmed = models.BooleanField(default=False)
  cancelled = models.BooleanField(default=False)
  
  

  class Meta:
    ordering = ['date']