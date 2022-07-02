
from django.urls import path
from apps.group_sessions import views

urlpatterns = [
   

    path('group-signup/', views.liveSessionsList, name='group-signup'), 
    path('group-signup-confirmation/<str:pk>/', views.groupSignUpConfirmation, name='group-signup-confirmation'), 
    path('group-session-cancellation/<str:pk>/', views.groupBookingCancellation, name='group-session-cancellation'), 
      

     path('leave-group/<str:pk>/', views.clientLeaveGroup, name='leave-group'),


    path('service-provider/schedule-group-sessions/<str:username>/', views.scheduleGroupSessions, name='schedule-group-sessions'),
    path('service-provider/available-group-sessions/<str:username>/', views.availableGroupSessions, name='available-group-sessions'),
    path('edit-group-session/<str:pk>/', views.updateGroupSession, name='edit-group-session'), 
 
    path('client/client-group-sessions/<str:username>/', views.clientGroupSessions, name='client-group-sessions'), 
   
    path('group-sessions-category-search/<slug>/', views.searchByCategory, name='group-sessions-category-search'), 
    path('group-sessions-text-search', views.searchByText, name='group-sessions-text-search'), 

]
