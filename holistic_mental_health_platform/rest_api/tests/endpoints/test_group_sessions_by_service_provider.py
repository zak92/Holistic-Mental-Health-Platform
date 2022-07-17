from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class GroupSessionsByServiceProviderTest(APITestCase):
  
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

    self.service_provider = ServiceProvider.objects.create(
      user=self.user_2,
      about="My name is Tom.",
      announcements='In a meeting!'
    )
    self.service_provider.save()

    self.group_booking = GroupBooking.objects.create(
      service_provider=self.user_2,
      group_name='Group 1',
      description='This is group 1.',
      category=Category.objects.create(title='Nutrition'), 
      date='2023-08-15',
      time='14:06:00',
      max_members=20,
      duration=60
      )
    self.group_booking.save()
    self.group_booking.members.add(self.user.id)

    self.good_url = reverse('api-group-sessions-by-sp')
    self.bad_url = '/service-provider-group-sessions'
    
  def tearDown(self):
    self.user.delete()
    self.user_2.delete()
    self.client_user.delete()
    self.service_provider.delete()
    self.group_booking.delete()
   

  def test_endpoint_accessible_on_good_url(self):
    '''test for 200 response code for user endpoint and logged in users'''
    self.client.login(username=self.user_2.username, password='12test1@1542')
    response = self.client.get(self.good_url)
    # test if the http code is 404
    self.assertEqual(response.status_code, 200)
  
  def test_endpoint_inaccessible_for_anonymous_users(self):
    '''test anonymous or logged out users'''
    response = self.client.get(self.good_url)
    self.assertNotEqual(response.status_code, 200)
  
  def test_endpoint_inaccessible_for_other_logged_in_users(self):
    '''test endpoint is not accessible for other logged in users (not the current user)'''
    self.client.login(username=self.user.username, password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertNotEqual(response.status_code, 200)


  def test_fail_on_bad_url(self):
    '''test for 404 response code for user endpoint'''
    response = self.client.get(self.bad_url)
    # test if the http code is 404
    self.assertEqual(response.status_code, 404)

  def test_endpoint_has_correct_field(self):
    self.client.login(username=self.user_2.username, password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertTrue('service_provider' in data['results'][0])
    self.assertTrue('members' in data['results'][0])
    self.assertTrue('category' in data['results'][0])
    self.assertTrue('group_name' in data['results'][0]) 
    self.assertTrue('description' in data['results'][0]) 
    self.assertTrue('date' in data['results'][0]) 
    self.assertTrue('time' in data['results'][0]) 
    self.assertTrue('max_members' in data['results'][0]) 
    self.assertTrue('duration' in data['results'][0]) 

  def test_endpoint_has_correct_field_values(self):
    self.client.login(username=self.user_2.username, password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertEqual(data['results'][0]['service_provider'], 'tom45')
    self.assertEqual(data['results'][0]['members'][0], 'kristy')
    self.assertEqual(data['results'][0]['group_name'], 'Group 1')
    self.assertEqual(data['results'][0]['description'], 'This is group 1.')
    self.assertEqual(data['results'][0]['category']['title'], 'Nutrition')
    self.assertEqual(data['results'][0]['date'], '2023-08-15')
    self.assertEqual(data['results'][0]['time'], '14:06:00')
    self.assertEqual(data['results'][0]['max_members'], 20)
    self.assertEqual(data['results'][0]['duration'], 60)
    self.assertEqual(data['results'][0]['cancelled'], False)
  

    