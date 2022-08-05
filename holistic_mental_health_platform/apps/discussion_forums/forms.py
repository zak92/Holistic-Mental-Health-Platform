from django import forms
from django.forms import ModelForm

from .models import *
from django.db import transaction


class CreateDiscussionPostForm(ModelForm):
  category = forms.ModelChoiceField(queryset = Category.objects.all())
  class Meta:
    model = DiscussionForumPost
    fields = ['title', 'category', 'discussion_post']

  def __init__(self,*args,**kwargs):
    super(CreateDiscussionPostForm,self).__init__(*args,**kwargs)

    self.fields["title"].label="Title"
    self.fields["title"].widget=forms.TextInput(attrs={"class":"form-control", 
    "style": "width:60%;padding:0.5em;"})


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
