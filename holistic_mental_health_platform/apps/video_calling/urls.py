from django.urls import path
from apps.video_calling import views

urlpatterns = [
   
  path('lobby/', views.lobby, name='lobby'),
  path('room/', views.conferenceRoom, name='room'),

  path('get_token/', views.getToken),

  path('create_member/', views.createMember),
  path('get_member/', views.getMember),
  path('delete_member/', views.deleteMember),
   
]
  # http://127.0.0.1:8080/video-calling/lobby/
