from django.db import models
from ..user_accounts.models import *
from django.shortcuts import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.

# https://www.youtube.com/watch?v=YXmsi13cMhw

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url_forums(self):
        return reverse("discussion-post-category-search", kwargs={
            "slug":self.slug
        })
    def get_url_blog(self):
        return reverse("blog-category-search", kwargs={
            "slug":self.slug
        })

    def get_url_group_sessions(self):
        return reverse("group-sessions-category-search", kwargs={
            "slug":self.slug
        })
  
  

  
    

class Comment(models.Model):
   author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   comment = models.TextField(null=True)
   flagged = models.BooleanField(default=False)
   date = models.DateTimeField(auto_now_add=True)
   def __str__(self):
        return self.comment

   class Meta:
    ordering = ['-date']


class DiscussionForumPost(models.Model):
  author = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=80, null=True) 
  slug = models.SlugField(max_length=80, unique=True, blank=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)# NULL=fALSE
  discussion_post = RichTextField(null=True)
  comments = models.ManyToManyField(Comment, related_name="comments", blank=True)
  flagged = models.BooleanField(default=False)
  date_created = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.title
 



  def save(self, *args, **kwargs):
      if not self.slug:
          self.slug = slugify(self.title)
      super(DiscussionForumPost, self).save(*args, **kwargs)

  def get_url(self):
      return reverse("discussion-post", kwargs={
          "slug":self.slug
      })

  class Meta:
    ordering = ['-date_created']