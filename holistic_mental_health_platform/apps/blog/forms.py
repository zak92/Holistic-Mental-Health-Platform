from django import forms
from django.forms import ModelForm
from .models import *


class CreateArticleForm(ModelForm):
  category = forms.ModelChoiceField(queryset = Category.objects.all())
  class Meta:
    model = Article
    fields = [ 'title', 'category', 'thumbnail_image', 'body']
  
  def __init__(self,*args,**kwargs):
    super(CreateArticleForm,self).__init__(*args,**kwargs)

    self.fields["title"].label="Title"
    self.fields["title"].widget=forms.TextInput(attrs={"class":"form-control", 
    "style": "width:60%;padding:0.5em;"})


    self.fields["thumbnail_image"].label="Thumbnail image"
    self.fields["thumbnail_image"].widget=forms.FileInput(attrs={"class":"form-control",
    "style": "width:50%;background-color: #FFC3C3;color: white;border-radius: 1em;margin-bottom:1em;margin-left:1em;"})
