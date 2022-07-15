from django.test import TestCase
import json
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class AllUsersTest(APITestCase):
  
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

    self.user_2 = User.objects.create_user(  
      id=2,
      username='tom45',
      password='12test1@1542', 
      email='tommy@example.com',
      country='Spain',
      city='Seville'
    )
    self.user_2.is_service_provider = True
    self.user_2.save()

    self.client_user = Client.objects.create(
      user=self.user,
      bio="My name is Kristy",
      status='Busy!'
    )
    self.client_user.save()

    self.service_provider = ServiceProvider.objects.create(
      user=self.user_2,
      about="My name is Tom.",
      announcements='In a meeting!'
    )
    self.service_provider.save()

    self.good_url = reverse('api-all-users')
    self.bad_url = '/api-all-users/'

    self.UserSerializer = UserSerializer(instance=self.user)
    
  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.service_provider.delete()
   

  def test_endpoint_accessible_on_good_url(self):
    '''test for 200 response code for user endpoint'''
    response = self.client.get(self.good_url)
    # test if the http code is 404
    self.assertEqual(response.status_code, 200)

  def test_fail_on_bad_url(self):
    '''test for 404 response code for user endpoint'''
    response = self.client.get(self.bad_url)
    # test if the http code is 404
    self.assertEqual(response.status_code, 404)

  def test_client_user_endpoint_has_correct_fields(self):
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertIsInstance(data, dict)
    self.assertIsInstance(data['results'], list)
    self.assertTrue('username' in data['results'][0])
    self.assertTrue('email' in data['results'][0])
    self.assertTrue('city' in data['results'][0])
    self.assertTrue('country' in data['results'][0]) 
    self.assertTrue('profile_picture' in data['results'][0]) 
    self.assertTrue('client' in data['results'][0]) 
    

  def test_client_user_endpoint_has_correct_field_values(self):
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertEqual(data['results'][0]['username'], 'kristy')
    self.assertEqual(data['results'][0]['email'], 'test@example.com')
    self.assertEqual(data['results'][0]['city'], 'Madrid')
    self.assertEqual(data['results'][0]['profile_picture'], 'http://testserver/media/user.png')
    self.assertEqual(data['results'][0]['client']['bio'], 'My name is Kristy')
    self.assertEqual(data['results'][0]['client']['status'], 'Busy!')
    

