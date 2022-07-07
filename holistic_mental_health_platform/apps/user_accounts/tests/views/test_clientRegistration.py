from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from ...views import *  
import json

class ClientRegistrationViewTest(TestCase):

  def setUp(self):
    self.factory = RequestFactory()
    self.good_url = reverse('registration')
    self.bad_url = '/registrations/'

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    response = self.client.get('/accounts/registration/client')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'user_accounts/clients_registration.html')

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_correct_response(self):
    response = self.client.get(self.good_url, format='json')
    # check if csrf token is present
    self.assertContains(response, 'csrfmiddlewaretoken')
    # Check that the response contains a form.
    self.assertContains(response, '<form')

  def test_create_new_client_user_POST(self):
    '''Test POST data, status code and redirect url'''
    data = {
      'username': 'user',
      'email': "user@mp.com", 
      'password1': "urt@hello123", 
      'password2': "urt@hello123",
      'agree': 'True'
    }
    response = self.client.post(self.good_url, data, follow=True)
    status_code = response.status_code
    redirect_path = response.request.get("PATH_INFO")
    self.assertEqual(redirect_path, reverse('home'))
    self.assertEqual(status_code, 200)

  


   
    
