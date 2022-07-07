from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
from ...forms import * 
import json


class UpdateServiceProviderProfileViewTest(TestCase):
  
  def setUp(self):
    self.factory = RequestFactory()
    self.user = User.objects.create_user( 
      id=1,
      username='jane_therapist',
      password='12test122', 
      email='jane@example.com',
      country='California',
      city='Sacramento'
    )
    self.user.save()
    self.service_provider_user = ServiceProvider.objects.create(
      user=self.user,
      about="My name is Jane",
      announcements='No appointments available'
    )
    self.service_provider_user.save()
    self.good_url = reverse('edit-service-provider-profile', kwargs={ 'username': 'jane_therapist'})
    self.bad_url = '/edit-sp-profile/'

  def tearDown(self):
    self.user.delete()
    self.service_provider_user.delete()

  def test_url_accessible_by_name(self):
    request = self.factory.get(self.good_url)
    # logged-in user
    request.user = self.user 
    response = updateServiceProviderProfile(request, 'jane_therapist')
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location_logged_in_user(self):
    request = self.factory.get('/profiles/edit-service-provider-profile/jane_therapist')
    # logged-in user
    request.user = self.user
    response = updateServiceProviderProfile(request, 'jane_therapist')
    self.assertEqual(response.status_code, 200)

  def test_logged_in_uses_correct_template(self):
    login = self.client.login(username='jane_therapist', password='12test122')
    response = self.client.get(self.good_url, format='json')
    # Check our user is logged in
    self.assertEqual(str(response.context['user']), 'jane_therapist')
    # Check that we got a response "success"
    self.assertEqual(response.status_code, 200)
    # Check we used correct template
    self.assertTemplateUsed(response, 'user_profiles/edit_service_provider_profile.html')

  def test_correct_response(self):
    self.client.login(username='jane_therapist', password='12test122')
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    # check if csrf token is present
    self.assertContains(response, 'csrfmiddlewaretoken')
    # Check that the response contains a form.
    self.assertContains(response, '<form')

  def test_fail_bad_url(self):
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)


## ADD MORE TESTS HERE