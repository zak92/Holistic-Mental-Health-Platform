from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class ServiceProviderProfileViewTest(TestCase):

  def setUp(self):
    self.factory = RequestFactory()
    self.user = User.objects.create_user( 
      id=1,
      username='jane_therapist',
      password='12test12', 
      email='jane@example.com',
      country='Spain',
      city='Seville'
    )
    self.user.save()
    self.service_provider_user = ServiceProvider.objects.create(
      user=self.user,
      about="My name is Jane and I am a therapist.",
      announcements='I will not be accepting appointments for the next two weeks!'
    )
    self.service_provider_user.save()
    self.good_url = reverse('service-provider-profile', kwargs={'username': 'jane_therapist'})
    self.bad_url = '/service-provider-profiles/'

  def tearDown(self):
    self.user.delete()
    self.service_provider_user.delete()
    
  def test_url_accessible_by_name(self):
    request = self.factory.get(self.good_url)
    # logged-in user
    request.user = self.user
    response = serviceProviderProfile(request, 'jane_therapist')
    self.assertEqual(response.status_code, 200)
  
  def test_url_exists_at_location_logged_in_user(self):
    request = self.factory.get('/profiles/service-provider/jane_therapist')
    # logged-in user
    request.user = self.user
    response = serviceProviderProfile(request, 'jane_therapist')
    self.assertEqual(response.status_code, 200)

  def test_url_exists_anonymous_user(self):
    request = self.factory.get('/profiles/service-provider/jane_therapist')
    # anonymous user
    request.user = AnonymousUser()
    response = serviceProviderProfile(request, 'jane_therapist')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'user_profiles/service_provider_profile.html')

  def test_correct_response(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Seville', response.content)
    self.assertIn(b'jane@example.com', response.content)
    self.assertIn(b'My name is Jane and I am a therapist.', response.content)
    self.assertIn(b'I will not be accepting appointments for the next two weeks!', response.content)
    
  def test_fail_bad_url(self):
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)