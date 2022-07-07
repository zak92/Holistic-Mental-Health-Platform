from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
from ...forms import * 
import json

class ChangePasswordViewTest(TestCase):
  
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
    self.user.save()

    self.good_url = reverse('change-password')
    self.bad_url = '/changepassword/'
  
  def tearDown(self):
    self.user.delete()

  def test_url_accessible_by_name(self):
    request = self.factory.get(self.good_url)
    # logged-in user
    request.user = self.user 
    response = changePassword(request)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location_logged_in_user(self):
    request = self.factory.get('/profiles/change-password')
    # logged-in user
    request.user = self.user
    response = changePassword(request)
    self.assertEqual(response.status_code, 200)

  def test_correct_response(self):
    self.client.login(username='kristy', password='12test12')
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    # check if csrf token is present
    self.assertContains(response, 'csrfmiddlewaretoken')
    # Check that the response contains a form.
    self.assertContains(response, '<form')

  def test_logged_in_uses_correct_template(self):
    self.client.login(username='kristy', password='12test12')
    response = self.client.get(self.good_url, format='json')
    # Check our user is logged in
    self.assertEqual(str(response.context['user']), 'kristy')
    # Check that we got a response "success"
    self.assertEqual(response.status_code, 200)
    # Check we used correct template
    self.assertTemplateUsed(response, 'user_profiles/password_change.html')

  def test_fail_bad_url(self):
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)


## ADD MORE TESTS HERE


  # def tests_change_password_post(self):
  #    self.client.login(username='kristy', password='12test12')
  #    response = self.client.post(self.good_url, {
  #      'old_password': '12test12',
  #      'new_password1': 'abcdefg123',
  #      'new_password2': 'abcdefg123'
  #    })

  #    #self.assertEqual(response.status_code, 302)
  #    #self.assertEqual(self.user.password, 'abcdefg123')