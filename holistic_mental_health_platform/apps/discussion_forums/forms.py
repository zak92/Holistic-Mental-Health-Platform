from django import forms
from django.forms import ModelForm

from .models import *
from django.db import transaction


class CreateDiscussionPostForm(ModelForm):
  category = forms.ModelChoiceField(queryset = Category.objects.all())
  class Meta:
    model = DiscussionForumPost
    fields = ['title', 'discussion_post', 'category']
    

class FlagDiscussionPostForm(ModelForm):
  
  class Meta:
    model = DiscussionForumPost
    fields = ['flagged']
    widgets = {'flagged': forms.HiddenInput()}

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.flagged = True
    user.save() 
    return user
