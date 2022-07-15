from django.urls import path
from . import api

urlpatterns = [
    path('user/<str:username>/', api.UserByUsername.as_view(), name='api-user'),
    path('users', api.AllUsers.as_view(), name='api-all-users'),

    path('blog-articles', api.AllBlogArticles.as_view(), name='api-blog-articles'),
    path('blog-by-category/<str:category>/', api.BlogArticleByCategory.as_view(), name='api-blog-by-category'),
    path('blog-article/<str:pk>/', api.BlogArticleByID.as_view(), name='api-blog-by-id'),

    path('all-discussions', api.AllDiscussions.as_view(), name='api-all-discussions'),
    path('discussions-by-category/<str:category>/', api.DiscussionsByCategory.as_view(), name='api-discussions-by-category'),
    path('discussion/<str:pk>/', api.DiscussionByID.as_view(), name='api-discussion-by-id'), 

    path('service-provider-bookings', api.AllBookingsByServiceProvider.as_view(), name='api-bookings-by-sp'),
    path('client-bookings', api.ClientBookings.as_view(), name='api-client-bookings'), 

    path('group-sessions', api.AllGroupSessions.as_view(), name='api-all-group-sessions'),
    path('group-sessions-by-category/<str:category>/', api.GroupSessionsByCategory.as_view(), name='api-group-sessions-by-category'),
    path('service-provider-group-sessions', api.GroupSessionsByServiceProvider.as_view(), name='api-group-sessions-by-sp'),
    path('client-group-sessions', api.ClientGroupSessions.as_view(), name='api-client-group-sessions'), 
    

    
   
]