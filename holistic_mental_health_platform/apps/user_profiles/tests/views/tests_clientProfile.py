from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class ClientProfileViewTest(TestCase):

  def setUp(self):
    self.factory = RequestFactory()
    self.user = User.objects.create_user( 
      id=1,
      username='kristy',
      password='12test12', 
      email='test@example.com',
      country='Spain',
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
    self.good_url = reverse('client-profile', kwargs={ 'username': 'kristy'})
    self.bad_url = '/client-profiles/x'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    
  def test_url_accessible_by_name(self):
    request = self.factory.get(self.good_url)
    # logged-in user
    request.user = self.user
    response = clientProfile(request, 'kristy')
    self.assertEqual(response.status_code, 200)
  
  def test_url_exists_at_location_logged_in_user(self):
    request = self.factory.get('/profiles/client/kristy')
    # logged-in user
    request.user = self.user
    response = clientProfile(request, 'kristy')
    self.assertEqual(response.status_code, 200)

  def test_url_exists_anonymous_user(self):
    '''Anonymous user can view this page'''
    request = self.factory.get('/profiles/client/kristy')
    # anonymous user
    request.user = AnonymousUser()
    response = clientProfile(request, 'kristy')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'user_profiles/client_profile.html')

  def test_correct_response(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    
  def test_fail_bad_url(self):
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)
