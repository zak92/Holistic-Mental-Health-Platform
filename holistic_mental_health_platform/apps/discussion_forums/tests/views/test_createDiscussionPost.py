from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class CreateDiscussionPostViewTest(TestCase):
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

    self.client_user = Client.objects.create(
      user=self.user,
      bio="My name is Jane and I am a therapist.",
      status='Busy!'
    )
    self.client_user.save()
   
    self.good_url = reverse('create-discussion-post')
    self.bad_url = '/create-discussion-post/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
   

  def test_url_accessible_by_name_only_for_logged_in_users(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location_only_for_logged_in_users(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get('/forums/create-discussion-post')
    self.assertEqual(response.status_code, 200)

  def test_url_inaccessible_at_for_anonymous_users(self):
    '''Anonymous users cannot access the page and are redirected to the login page'''
    response = self.client.get('/forums/create-discussion-post')
    self.assertNotEqual(response.status_code, 200)
    self.assertEqual(response.status_code, 302)

  def test_correct_response(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    # check if csrf token is present
    self.assertContains(response, 'csrfmiddlewaretoken')
    # Check that the response contains a form.
    self.assertContains(response, '<form')

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_create_new_discussion_POST(self):
    '''Test POST data, status code and redirect url'''
    self.client.login(username='jane26', password='12test1@1542')
    Category.objects.create(title='Nutrition')
   
    data = {
      'title': 'Nutrition',
      'category': Category.objects.get(title='Nutrition'),
      'discussion_post': 'This is the body of the post!',
      
    }
    response = self.client.post(self.good_url, data, follow=True)
    status_code = response.status_code
    self.assertEqual(status_code, 200)