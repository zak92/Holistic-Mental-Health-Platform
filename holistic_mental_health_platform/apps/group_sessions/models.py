from django.db import models
from django.forms import DateField
from ..user_accounts.models import *
from django.urls import reverse
from ..discussion_forums.models import Category
from django.utils.text import slugify
# Create your models here.


class GroupBooking(models.Model):
  service_provider = models.ForeignKey(User, related_name="service_provider_group_sessions", on_delete=models.CASCADE, null=True)
  members = models.ManyToManyField(User, related_name="members")
  group_name = models.CharField(max_length=70, null=True)
  description = models.CharField(max_length=500, null=True) 
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
  date = models.DateField(null=True)
  time = models.TimeField(null=True)
  max_members = models.IntegerField(null=True)
  duration = models.IntegerField(null=True)
  cancelled = models.BooleanField(default=False)

  def total_members(self):
    return self.members.count()

  def __str__(self):
    return self.group_name

  class Meta:
    ordering = ['date']