from cgitb import lookup
from apps.user_accounts.models import *
from apps.user_profiles.models import *
from apps.discussion_forums.models import *
from apps.blog.models import *
from apps.bookings.models import *
from apps.group_sessions.models import *
from django_countries.serializers import CountryFieldMixin

from rest_framework import serializers
import django_filters

 
class ClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Client
    fields = ['bio' , 'status']

class ServiceProviderSerializer(serializers.ModelSerializer):
  class Meta:
    model = ServiceProvider
    fields = ['about' , 'announcements']

class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
  client = ClientSerializer()
  service_provider = ServiceProviderSerializer(source='serviceprovider')
  class Meta:
    model = User
    fields = [
      'username', 'first_name', 'last_name', 'email', 'city', 'country', 'is_client', 
      'is_service_provider', 'profile_picture', 'client', 'service_provider'
      ]

      
class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['title','slug']

class BlogSerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField()
  category = CategorySerializer()
  class Meta:
    model = Article
    fields = ['pk', 'author', 'title', 'body', 'category', 'date_updated', 'thumbnail_image']

class CommentSerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField()
  class Meta:
    model = Comment
    fields = ['author', 'comment', 'flagged']


class DiscussionForumSerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField()
  category = CategorySerializer()
  comments = CommentSerializer(many=True)
  class Meta:
    model = DiscussionForumPost
    fields = ['pk', 'author', 'title', 'category', 'discussion_post', 'comments', 'flagged', 'date_created']

class BookingSerializer(serializers.ModelSerializer):
  service_provider = serializers.StringRelatedField()
  client = serializers.StringRelatedField()
  class Meta:
    model = Booking
    fields = ['service_provider', 'date', 'time', 'client', 'booked', 'confirmed', 'cancelled']
    

class GroupSessionSerializer(serializers.ModelSerializer):
  service_provider = serializers.StringRelatedField()
  members = serializers.StringRelatedField(many=True)
  category = CategorySerializer()
  class Meta:
    model = GroupBooking
    fields = [
      'service_provider', 'members', 'group_name', 'description', 
      'category', 'date', 'time', 'max_members', 'duration','cancelled'
      ]












