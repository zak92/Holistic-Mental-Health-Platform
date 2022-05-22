from email.quoprimime import body_check
from django.db import models
from django.forms import CharField, SlugField
from django.urls import reverse
from ..users.models import *
# Create your models here.


class Article(models.Model):
  EXERCISE = 'EX'
  GENERAL = 'GN'
  NUTRITION = 'NT'

  TOPIC_CHOICES = [
      (EXERCISE, 'Exercise'),
      (NUTRITION, 'Nutrition'),
      (GENERAL, 'General')
  ]


  title = models.CharField(max_length=100)
  #topic = models.CharField(max_length=2,choices=TOPIC_CHOICES,default=GENERAL)
  slug = models.SlugField(null=False, unique=True)
  body = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  thumb = models.ImageField(default="test.jpg", null=True)
  author = models.ForeignKey(User, default=None,  on_delete=models.DO_NOTHING)
  # date_updated
  # add in thumbnail
  # add in author
  def __str__(self):
    return self.title

  def get_absolute_url(self):
        return reverse("blogPost", kwargs={"slug": self.slug})