from django.urls import path
from apps.video_calling import views

urlpatterns = [
   
  path('lobby/', views.lobby, name='lobby'),
  path('room/', views.conferenceRoom, name='room'),

  path('get_token/', views.getToken, name='get-token'),

  path('create_member/', views.createMember, name='create-member'),
  path('get_member/', views.getMember, name='get-member'),
  path('delete_member/', views.deleteMember, name='delete-member'),
   
]

