from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

# https://www.valentinog.com/blog/testing-django/
# https://www.oreilly.com/library/view/test-driven-development-with/9781449365141/ch11.html
# For forms - https://fossies.org/linux/Django/tests/auth_tests/test_forms.py
# https://www.youtube.com/watch?v=qwypH3YvMKc&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM
# https://docs.djangoproject.com/en/4.0/topics/testing/tools/#overview-and-a-quick-example
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
# https://stackoverflow.com/questions/37363218/django-testing-the-html-of-your-homepage-against-the-content-of-a-response

# Models https://www.youtube.com/watch?v=GBgRMdjAx_c&list=PLOLrQ9Pn6cay7t8VZ3wmn6QdAxzTx60F3&index=2
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
    #self.assertIn(b'Madrid', response.content)
    # self.assertIn(b'test@example.com', response.content)
    # self.assertIn(b'My name is Kristy', response.content)
    # self.assertIn(b'Busy!', response.content)
    
  def test_fail_bad_url(self):
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)
