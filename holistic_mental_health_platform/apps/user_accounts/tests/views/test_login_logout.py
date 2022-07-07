from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class LoginViewTest(TestCase):

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
    self.good_url = reverse('login')
    self.bad_url = '/login/'
    
  def tearDown(self):
    self.user.delete()
    self.client_user.delete()

  def test_user_exists(self):
    '''Test that the user exists'''
    user_account = User.objects.all().count()
    self.assertEqual(user_account, 1)

  def test_user_password(self):
    '''Check that the password is correct'''
    user_a = User.objects.get(username='jane26')
    self.assertTrue(user_a.check_password('12test1@1542'))

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    response = self.client.get('/accounts/login')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'user_accounts/login.html')

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

  def test_login_user_POST(self):
    '''Test POST data, status code and redirect url'''
    data = {
      'username': 'jane26',
      'password': '12test1@1542', 
    }
    response = self.client.post(self.good_url, data, follow=True)
    status_code = response.status_code
    redirect_path = response.request.get("PATH_INFO")
    self.assertEqual(redirect_path, reverse('home'))
    self.assertEqual(status_code, 200)

  def test_login_failed_username_or_password_incorrect(self):
    '''login failed because user does not exist'''
    data = {
      'username': 'jane8926',
      'password': '12test1@15542', 
    }
    response = self.client.post(self.good_url, data, follow=True)
    messages = list(response.context['messages'])
    # login failed message is displayed to the user
    self.assertEqual(str(messages[0]), 'Username or password is incorrect')


  def logout(self):
    '''logo out'''
    self.client.logout()

  def test_get_logout(self):
    '''Test logout, status code and redirect url'''
    self.logout()
    response = self.client.get(self.good_url)
    status_code = response.status_code
    redirect_path = response.request.get("PATH_INFO")
    self.assertEqual(redirect_path, reverse('login'))
    self.assertEqual(status_code, 200)
    
  