from django import forms
from django.forms import ModelForm
from .models import *


class CreateArticleForm(ModelForm):
  category = forms.ModelChoiceField(queryset = Category.objects.all())
  class Meta:
    model = Article
    fields = [ 'title', 'category', 'thumbnail_image', 'body']
  
