from django.urls import path
from . import api

urlpatterns = [
    path('user/<str:username>/', api.User.as_view(), name='api-user'),

    path('blog-articles', api.AllBlogArticles.as_view(), name='api-blog-articles'),
    path('blog-by-category/<str:category>/', api.BlogArticleByCategory.as_view(), name='api-blog-by-category'),
    path('blog-article/<str:pk>/', api.BlogArticleByID.as_view(), name='api-blog-by-id'),
   
   
]