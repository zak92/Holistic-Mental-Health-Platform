from cgitb import lookup
from apps.user_accounts.models import *
from apps.user_profiles.models import *
from apps.blog.models import *
from django_countries.serializers import CountryFieldMixin

from rest_framework import serializers
import django_filters

# https://sunscrapers.com/blog/ultimate-tutorial-django-rest-framework-part-1/
 
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
            fields = ('title','slug')

class AllBlogArticlesSerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField()
  category = CategorySerializer()
  class Meta:
    model = Article
    fields = ['pk', 'author', 'title', 'body', 'category', 'date_updated', 'thumbnail_image']

class BlogArticleByIDSerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField()
  category = CategorySerializer()
  class Meta:
    model = Article
    fields = ['author', 'title', 'body','category', 'date_updated', 'thumbnail_image']

class BlogArticleByCategorySerializer(serializers.ModelSerializer):
  author = serializers.StringRelatedField()
  category = CategorySerializer()
  class Meta:
    model = Article
    fields = ['author', 'title', 'body','category', 'date_updated', 'thumbnail_image']









