from django import forms
from django.forms import ModelForm
from .models import *


class CreateArticle(ModelForm):
  class Meta:
    model = Article
    fields = ['title', 'body', 'slug', 'thumb']
    widgets = {'slug': forms.HiddenInput()}