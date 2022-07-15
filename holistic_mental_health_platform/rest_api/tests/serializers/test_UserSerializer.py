from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class UserSerializerTest(APITestCase):
  
  def setUp(self):
    self.user = User.objects.create_user( 
      id=1,
      username='kristy',
      password='12test12', 
      email='test@example.com',
      country='',
      city='Madrid'
    )
    self.user.is_client = True
    self.user.save()
    self.client_user = Client.objects.create(
      user=self.user,
      bio="My name is Kristy",
      status='Busy!'
    )
    self.client_user.save()

    self.UserSerializer = UserSerializer(instance=self.user)
    
  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
   

  def test_client_user_serializer_has_correct_fields(self):
    '''check if all the necessary fields are correct'''
    data = self.UserSerializer.data 
    self.assertEqual(set(data.keys()), set( 
      [
      'username', 'first_name', 'last_name', 'email', 'city', 'country', 'is_client', 
      'is_service_provider', 'profile_picture', 'client', 'service_provider'
      ]
    ))
  
  def test_client_user_serializer_has_correct_field_values(self):
    '''check if all the the fields contain correct values'''
    data = self.UserSerializer.data
    # check if data is correct
    self.assertEqual(data['username'], 'kristy')
    self.assertEqual(data['first_name'], '')
    self.assertEqual(data['last_name'], '')
    self.assertEqual(data['email'], 'test@example.com')
    self.assertEqual(data['city'], 'Madrid')
    self.assertEqual(data['is_client'], True)
    self.assertEqual(data['is_service_provider'], False)
    self.assertEqual(data['profile_picture'], '/media/user.png')
    self.assertEqual(data['client']['bio'], 'My name is Kristy')
    self.assertEqual(data['service_provider'], None)