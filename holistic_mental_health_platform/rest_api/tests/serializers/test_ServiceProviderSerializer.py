from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class ServiceProviderSerializerTest(APITestCase):
  
  def setUp(self):

    self.user = User.objects.create_user(  
      id=1,
      username='tom45',
      password='12test1@1542', 
      email='tommy@example.com',
      country='Spain',
      city='Seville'
    )
    self.user.is_service_provider = True
    self.user.save()

    self.service_provider = ServiceProvider.objects.create(
      user=self.user,
      about="My name is Tom.",
      announcements='In a meeting!'
    )
    self.service_provider.save()


    self.ServiceProviderSerializer = ServiceProviderSerializer(instance=self.service_provider)
    
  def tearDown(self):
    self.user.delete()
    self.service_provider.delete()
   

  def test_serializer_has_correct_fields(self):
    '''check if all the necessary fields are correct'''
    data = self.ServiceProviderSerializer.data 
    self.assertEqual(set(data.keys()), set( 
     ['about' , 'announcements']
    ))
    
  
  def test_serializer_has_correct_field_values(self):
    '''check if all the the fields contain correct values'''
    data = self.ServiceProviderSerializer.data
    # check if data is correct
    self.assertEqual(data['about'], 'My name is Tom.')
    self.assertEqual(data['announcements'], 'In a meeting!')
    