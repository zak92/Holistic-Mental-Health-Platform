from turtle import title
from apps.user_accounts.models import *
from apps.user_profiles.models import *
from apps.blog.models import *
from .serializers import *

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

from rest_framework import permissions

import datetime
from datetime import datetime


from django_filters.rest_framework import DjangoFilterBackend

# Custom permissions - only the current user can have access to an api view
class CustomUserPermission(permissions.BasePermission):
  message = 'Restricted to the owner'

  def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
  def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserByUsername(mixins.CreateModelMixin,
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
        

class AllUsers(generics.ListAPIView):

  # select the appropriate queryset and  serializer
  queryset = User.objects.all()
  serializer_class = UserSerializer


class AllBlogArticles(generics.ListAPIView):
  queryset = Article.objects.all()
  serializer_class = BlogSerializer

class BlogArticleByID(generics.ListAPIView):
  queryset = Article.objects.all()
  serializer_class = BlogSerializer

  def get_queryset(self):
    pk = self.kwargs['pk']
    return Article.objects.filter(pk=pk)

class BlogArticleByCategory(generics.ListAPIView):

  lookup_field = 'category'
  serializer_class = BlogSerializer

  def get_queryset(self):
    category = self.kwargs['category']
    category_id = Category.objects.get(slug=category)
    return Article.objects.filter(category=category_id.id)

class DiscussionByID(generics.ListAPIView):
  queryset = DiscussionForumPost.objects.all()
  serializer_class = DiscussionForumSerializer

  def get_queryset(self):
    pk = self.kwargs['pk']
    return DiscussionForumPost.objects.filter(pk=pk)

class AllDiscussions(generics.ListAPIView):
  queryset = DiscussionForumPost.objects.all()
  serializer_class = DiscussionForumSerializer
    
class DiscussionsByCategory(generics.ListAPIView):

  lookup_field = 'category'
  serializer_class = DiscussionForumSerializer

  def get_queryset(self):
    category = self.kwargs['category']
    category_id = Category.objects.get(slug=category)
    return DiscussionForumPost.objects.filter(category=category_id.id)

# only the logged in and current user (request.user) can access their information
class AllBookingsByServiceProvider(generics.ListAPIView):
  #lookup_field = 'username'
  serializer_class =  BookingSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    #username = self.kwargs['username']
    #user_id = User.objects.get(username=username)
    current_date = datetime.now().date()  
    current_time = datetime.now().time()  
    # filter by request.user - only show valid bookings 
    #return Booking.objects.filter(service_provider=user_id.id).filter(date__gte=current_date)
    return Booking.objects.filter(service_provider=self.request.user).filter(date__gte=current_date)

# only the logged in and current user (request.user) can access their information
class ClientBookings(generics.ListAPIView, CustomUserPermission):
  #lookup_field = 'username'
  serializer_class = BookingSerializer
  permission_classes = [permissions.IsAuthenticated]

  

  def get_queryset(self):
    # username = self.kwargs['username']
    # user_id = User.objects.get(username=username)
    current_date = datetime.now().date()   
    # filter by request.user - only show valid bookings 
    return Booking.objects.filter(client=self.request.user).filter(date__gte=current_date)

class AllGroupSessions(generics.ListAPIView):
  serializer_class = GroupSessionSerializer

  def get_queryset(self):
    current_date = datetime.now().date()  
    # filter by request.user - only show valid bookings 
    return GroupBooking.objects.filter(cancelled=False).filter(date__gte=current_date)

class GroupSessionsByCategory(generics.ListAPIView):
  lookup_field = 'category'
  serializer_class = GroupSessionSerializer

  def get_queryset(self):
    current_date = datetime.now().date()  
    category = self.kwargs['category']
    category_id = Category.objects.get(slug=category)
    # filter by request.user - only show valid bookings 
    return GroupBooking.objects.filter(cancelled=False).filter(category=category_id.id).filter(date__gte=current_date)

# only the logged in and current user (request.user) can access their information
class GroupSessionsByServiceProvider(generics.ListAPIView):
  #lookup_field = 'username'
  serializer_class = GroupSessionSerializer
  permission_classes = [permissions.IsAuthenticated]


  def get_queryset(self):
    current_date = datetime.now().date()  
    # username = self.kwargs['username']
    # user_id = User.objects.get(username=username)
    current_date = datetime.now().date() 
    # filter by request.user - only show valid bookings 
    return GroupBooking.objects.filter(cancelled=False).filter(service_provider=self.request.user).filter(date__gte=current_date)

# only the logged in and current user (request.user) can access their information
class ClientGroupSessions(generics.ListAPIView, CustomUserPermission):
  #lookup_field = 'username'
  serializer_class = GroupSessionSerializer
  permission_classes = [permissions.IsAuthenticated] 
  

  def get_queryset(self):
    current_date = datetime.now().date()  
    # username = self.kwargs['username']
    # user_id = User.objects.get(username=username)
    current_date = datetime.now().date() 
    # filter by request.user - only show valid bookings 
    return GroupBooking.objects.filter(cancelled=False).filter(members=self.request.user).filter(date__gte=current_date)

        


