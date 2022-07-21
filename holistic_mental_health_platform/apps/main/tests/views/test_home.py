from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json


class HomeViewTest(TestCase):
  def setUp(self):
   
    self.good_url = reverse('home')
    self.bad_url = '/home/'


  def test_url_accessible_by_name(self):
    '''test if url is accessible by name'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    '''test if url is accessible by location'''
    response = self.client.get('')
    self.assertEqual(response.status_code, 200)
  
  def test_uses_correct_template_logged_in_sp(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'main/home.html')

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)