from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json


class AvailableGroupSessionsViewTest(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.user = User.objects.create_user(  
      id=1,
      username='jack26',
      password='12test1@1542', 
      email='jack26@example.com',
      country='Spain',
      city='Madrid'
    )
    self.user.is_service_provider = True
    self.user.save()
  
    self.user_2 = User.objects.create_user(  
      id=2,
      username='jane26',
      password='12test1@1542', 
      email='jane26@example.com',
      country='Spain',
      city='Madrid'
    )
    self.user_2.is_client = True
    self.user_2.save()

    self.service_provider = ServiceProvider.objects.create(
      user=self.user,
      about="My name is Jack and I am a therapist.",
      announcements='On vacation for the next 2 weeks.'
    )
    self.service_provider.save()

    self.client_user = Client.objects.create(
      user=self.user_2,
      bio="My name is Jane.",
      status='Busy!'
    )
    self.client_user.save()
   
    self.group_booking = GroupBooking.objects.create(
      service_provider=self.user,
      group_name='Group 1',
      description='This is group 1.',
      category=Category.objects.create(title='Nutrition'), 
      date='2023-08-15',
      time='14:06:00',
      max_members=20,
      duration=60
      )
    self.group_booking.save()
    self.group_booking.members.add(self.user_2.id)

    self.good_url = reverse('available-group-sessions', kwargs={ 'username': 'jack26'})
    self.bad_url = '/available-group-sessions/jack26/'

  def tearDown(self):
    self.user.delete()
    self.user_2.delete()
    self.service_provider.delete()
    self.client_user.delete()
    self.group_booking.delete()

  def test_url_accessible_by_name_logged_in_sp(self):
    '''Only the logged in page owner can access this page'''
    self.client.login(username='jack26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location_logged_in_sp(self):
    '''Only the logged page owner can access this page'''
    self.client.login(username='jack26', password='12test1@1542')
    response = self.client.get('/group-sessions/service-provider/available-group-sessions/jack26/')
    self.assertEqual(response.status_code, 200)
  
  def test_page_unavailable_for_all_logged_out_users(self):
    '''Page not available for all logged out users'''
    response = self.client.get(self.good_url)
    # users get redirected to home page - code 302
    self.assertEqual(response.status_code, 302)
    

  def test_uses_correct_template_logged_in_sp(self):
    '''Test that the correct template is used for logged in post creator'''
    self.client.login(username='jack26', password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'group_sessions/sp_available_group_sessions.html')

  def test_page_unavailable_for_all_other_logged_in_users(self):
    '''Page not available for all logged out users (not the page owner)'''
    self.client.login(username='timmy', password='123test1@1542')
    response = self.client.get(self.good_url)
    # users get redirected to home page - code 302
    self.assertEqual(response.status_code, 302)
    

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)