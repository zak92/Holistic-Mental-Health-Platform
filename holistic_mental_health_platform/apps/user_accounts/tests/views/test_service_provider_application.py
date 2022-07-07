from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from ...views import *  
import json

class ServiceProviderApplicationViewTest(TestCase):

  def setUp(self):
    self.factory = RequestFactory()
    self.good_url = reverse('application')
    self.bad_url = '/application/'

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    response = self.client.get('/accounts/application/service-provider')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'user_accounts/service_providers_registration_application.html')

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

  def test_service_provider_application_POST(self):
    '''Test POST data, status code and redirect url'''
    data = {
      'first_name': 'Jack',
      'last_name': 'Dawson',
      'username': 'user25412',
      'email': 'user@mop.com', 
    }
    response = self.client.post(self.good_url, data, follow=True)
    status_code = response.status_code
    redirect_path = response.request.get("PATH_INFO")
    self.assertEqual(redirect_path, reverse('home'))
    self.assertEqual(status_code, 200)