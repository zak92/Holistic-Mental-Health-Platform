
from django.urls import path
from apps.discussion_forums import views

urlpatterns = [
   

    path('', views.forumHome, name='forum-home'), 
    path('discussion-post/<slug>/', views.discussionPost, name='discussion-post'), 
    path('discussion-post-category-search/<slug>/', views.searchByCategory, name='discussion-post-category-search'), 
    path('discussion-post-text-search', views.searchByText, name='discussion-post-text-search'), 
    path('create-discussion-post', views.createDiscussionPost, name='create-discussion-post'), 

    path('delete-discussion-post/<str:pk>/', views.deleteDiscussionPost, name='delete-discussion-post'), 
    path('update-discussion-post/<str:pk>/', views.updateDiscussionPost, name='update-discussion-post'),

    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    

   

]