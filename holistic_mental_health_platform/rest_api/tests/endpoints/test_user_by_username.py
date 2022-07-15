from django.test import TestCase
import json
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class UserTest(APITestCase):
  
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

    self.good_url = reverse('api-user', kwargs={'username': 'kristy'})
    self.bad_url = '/api-user/'

    self.UserSerializer = UserSerializer(instance=self.user)
    
  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    

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

  def test_client_user_endpoint_has_correct_field(self):
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertTrue('username' in data)
    self.assertTrue('email' in data)
    self.assertTrue('city' in data)
    self.assertTrue('country' in data) 
    self.assertTrue('profile_picture' in data) 
    self.assertTrue('client' in data) 
    

  def test_client_user_endpoint_has_correct_field_values(self):
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertEqual(data['username'], 'kristy')
    self.assertEqual(data['email'], 'test@example.com')
    self.assertEqual(data['city'], 'Madrid')
    self.assertEqual(data['profile_picture'], 'http://testserver/media/user.png')
    self.assertEqual(data['client']['bio'], 'My name is Kristy')
    self.assertEqual(data['client']['status'], 'Busy!')
    