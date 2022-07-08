from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class CancelBookingBySPViewTest(TestCase):
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

    self.booking = Booking.objects.create(
        service_provider = self.user_2,
        date = '2023-08-15',
        time = '14:06:00',
        client = self.user
    )

    self.booking.save()

    self.good_url = reverse('cancel-booking-sp', kwargs={ 'pk': 1})
    self.bad_url = '/cancel-booking-sp/'

  def tearDown(self):
    self.user.delete()
    self.user_2.delete()
    self.client_user.delete()
    self.service_provider.delete()
    self.booking.delete()

  def test_url_accessible_by_name_logged_in_user(self):
    user = User.objects.get(id=2)
    self.client.login(username=user.username, password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200) 

  def test_url_exists_at_location_logged_in_user(self):
    '''Accessible for request.user'''
    self.client.login(username='tom45', password='12test1@1542')
    response = self.client.get('/bookings/cancel-booking-sp/1/')
    self.assertEqual(response.status_code, 200)
    
  def test_url_redirect_for_logged_out_users(self):
    '''Test that logged out users gets redirected to login page'''
    response = self.client.get(self.good_url)
    # gets redirected to login page
    self.assertEqual(response.status_code, 302)

  def test_redirect_for_other_logged_in_users(self):
    '''Redirect for other logged in users (not request.user)'''
    user = User.objects.get(id=1)
    self.client.login(username=user.username, password='12test1@1542')
    response = self.client.get(self.good_url)
    # users get redirected to home page - code 302
    self.assertEqual(response.status_code, 302)

  def test_uses_correct_template_logged_in_user(self):
    '''Test that the correct template is used for logged in user'''
    self.client.login(username='tom45', password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    self.assertTemplateUsed(response, 'bookings/service_provider_cancel_booking.html')

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_cancel_booking_post_POST(self):
    '''Test that the booking has been cancelled by SP'''
    self.client.login(username='tom45', password='12test1@1542')
    self.booking.cancelled = True
    self.booking.save()
    response = self.client.post(self.good_url,  self.booking.__dict__, follow=True)
    self.booking.refresh_from_db()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(self.booking.cancelled,  True)