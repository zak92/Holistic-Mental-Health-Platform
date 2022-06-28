from django.urls import path
from apps.blog import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('create-blog-post', views.createBlogPost, name='create-blog-post'), 
    path('blog-home', views.blogHome, name='blog-home'), 
    path('article/<slug:slug>', views.blogPost, name='blog-post'), 
    path('blog-category-search/<slug>/', views.searchByCategory, name='blog-category-search'), 
    path('blog-text-search', views.searchByText, name='blog-text-search'),  

    path('delete-blog-post/<str:pk>/', views.deleteBlogPost, name="delete-blog-post"), 
    path('update-blog-post/<str:pk>/', views.updateBlogPost, name="update-blog-post"),  
    
    
]

