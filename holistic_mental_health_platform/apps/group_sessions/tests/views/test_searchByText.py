from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json
from django.db.models import Q


class SearchByTextViewTest(TestCase):
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

    self.group_booking_2 = GroupBooking.objects.create(
      service_provider=self.user,
      group_name='Group 2',
      description='This is group 2.',
      category=Category.objects.create(title='Mental Health'), 
      date='2023-09-15',
      time='14:06:00',
      max_members=20,
      duration=60
      )
    self.group_booking_2.save()

    self.good_url = reverse('group-sessions-text-search')
    self.bad_url = 'group-sessions-text-search'

  def tearDown(self):
    self.user.delete()
    self.user_2.delete()
    self.service_provider.delete()
    self.client_user.delete()
    self.group_booking.delete()
    self.group_booking_2.delete()

  def test_url_accessible_by_name(self):
    '''All users access this page'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    '''All users access this page'''
    response = self.client.get('/group-sessions/group-sessions-text-search')
    self.assertEqual(response.status_code, 200)

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'group_sessions/text_search_results.html')


  def test_search_function(self):
    '''Test if the search function gives the correct results'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    session_list = GroupBooking.objects.filter(
     Q(group_name__icontains='group 2') |                                                                              
     Q(description__icontains='group 2')
    ) 
    self.assertEqual(session_list[0].group_name, 'Group 2')
    self.assertEqual(session_list[0].description, 'This is group 2.')

