from turtle import title
from apps.user_accounts.models import *
from apps.user_profiles.models import *
from apps.blog.models import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend


class User(mixins.CreateModelMixin,
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,
            generics.GenericAPIView):

  lookup_field = 'username'
  # select the appropriate queryset and  serializer
  queryset = User.objects.all()
  serializer_class = UserSerializer

  # https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html

  # def get_queryset(self):
        
  #       return self.queryset.filter(is_client=True)
   # This function displays the data to the user in the browsable API interface
  def get(self, request, *args, **kwargs):
      return self.retrieve(request, *args, **kwargs)
        

# class AllUsers(generics.ListAPIView):

  
#   # select the appropriate queryset and  serializer
#   queryset = User.objects.all()
#   serializer_class = UserSerializer

class AllBlogArticles(generics.ListAPIView):
  queryset = Article.objects.all()
  serializer_class = AllBlogArticlesSerializer

class BlogArticleByID(generics.ListAPIView):
  queryset = Article.objects.all()
  serializer_class = BlogArticleByIDSerializer 

  def get_queryset(self):
    pk = self.kwargs['pk']
    return Article.objects.filter(pk=pk)

class BlogArticleByCategory(generics.ListAPIView):

  lookup_field = 'category'
  serializer_class = BlogArticleByCategorySerializer

  def get_queryset(self):
    category = self.kwargs['category']
    category_id = Category.objects.get(slug=category)
    return Article.objects.filter(category=category_id.id)
    
  
        


