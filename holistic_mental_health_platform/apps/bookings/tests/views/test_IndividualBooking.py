from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class BookIndividualAppointmentsViewTest(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.user = User.objects.create_user(  
      id=1,
      username='jane26',
      password='12test1@1542', 
      email='jane26@example.com',
      country='Spain',
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

    self.service_provider = ServiceProvider.objects.create(
      user=self.user_2,
      about="My name is Tom.",
      announcements='In a meeting!'
    )
    self.service_provider.save()

    self.client_user = Client.objects.create(
      user=self.user,
      bio="My name is Jane.",
      status='Busy!'
    )
    self.client_user.save()

    self.good_url = reverse('client-booking', kwargs={ 'username': 'jane26'})
    self.bad_url = '/booking-client/jane26'

  def tearDown(self):
    self.user.delete()
    self.user_2.delete()
    self.client_user.delete()
    self.service_provider.delete()
  

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200) 

  def test_url_exists_at_location(self):
    response = self.client.get('/bookings/booking-client/jane26/')
    self.assertEqual(response.status_code, 200)
  
  def test_uses_correct_template_logged_in_user(self):
    '''Test that the correct template is used for logged in user'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    self.assertTemplateUsed(response, 'bookings/booking_individual.html')

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)
