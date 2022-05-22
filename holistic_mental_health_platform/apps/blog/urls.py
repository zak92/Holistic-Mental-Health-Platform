from django.urls import path
from apps.blog import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('create-blog-post', views.createBlogPost, name='createBlogPost'), 
    path('article-list', views.articleList, name='articleList'), 
    path('article/<slug:slug>', views.blogPost, name='blogPost'), 
    
    
    
]