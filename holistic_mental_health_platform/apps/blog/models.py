from email.quoprimime import body_check
from django.db import models
from django.urls import reverse
from ..user_accounts.models import *
from ..discussion_forums.models import Category
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
  author = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100, unique=True, blank=True)
  body = RichTextField(null=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)
  thumbnail_image = models.ImageField(null=True)
  
  def __str__(self):
    return self.title
  

  def save(self, *args, **kwargs):
      if not self.slug:
          self.slug = slugify(self.title)
      super(Article, self).save(*args, **kwargs)

  def get_url(self):
      return reverse("blog-post", kwargs={
          "slug": self.slug
      })

  class Meta:
    ordering = ['-date_created']