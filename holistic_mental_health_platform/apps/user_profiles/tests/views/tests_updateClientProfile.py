from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
from ...forms import * 
import json

class UpdateClientProfileViewTest(TestCase):
  
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
    self.client_user = Client.objects.create(
      user=self.user,
      bio="My name is Kristy",
      status='Busy!'
    )
    self.client_user.save()
    self.good_url = reverse('edit-client-profile', kwargs={ 'username': 'kristy'})
    self.bad_url = '/edit-client-profile/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()

  def test_url_accessible_by_name(self):
    request = self.factory.get(self.good_url)
    # logged-in user
    request.user = self.user 
    response = updateClientProfile(request, 'kristy')
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location_logged_in_user(self):
    request = self.factory.get('/profiles/edit-client-profile/kristy')
    # logged-in user
    request.user = self.user
    response = updateClientProfile(request, 'kristy')
    self.assertEqual(response.status_code, 200)

  def test_logged_in_uses_correct_template(self):
    self.client.login(username='kristy', password='12test12')
    response = self.client.get(self.good_url, format='json')
    # Check our user is logged in
    self.assertEqual(str(response.context['user']), 'kristy')
    # Check that we got a response "success"
    self.assertEqual(response.status_code, 200)
    # Check we used correct template
    self.assertTemplateUsed(response, 'user_profiles/edit_client_profile.html')

  def test_correct_response(self):
    self.client.login(username='kristy', password='12test12')
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



  # def test_update_profile_POST(self):
  #   data = {
  #     'first_name': '',
  #     'last_name': '',
  #     'username': 'kristy',
  #     'email': 'kristy@gmail.com',
  #     'country': 'Spain',
  #     'city': 'Madrid',
  #     'profile_picture': 'kristy_mRGZ79I.jpg',
  #     'bio': 'My name is Kristy!',
  #     'status': 'In a meeting!'
  #   }
  #   request = self.factory.post('/profiles/edit-client-profile/kristy/', data=data, content_type='application/json')
  #   request.user = self.user 
  #   response = updateClientProfile(request, 'kristy')
    
    
    
    # request = self.factory.post('/profiles/edit-client-profile/kristy/', data=data, content_type='application/json')
    # response = updateClientProfile(request, 'kristy')
    # cat = User.objects.get(user=request.user)
    # print(cat.email)
    # Check that we got a response "redirect"
    # response = self.factory.post("/profiles/edit-client-profile/kristy/", data = {
    #   'username': 'kristy',
    #   'email': 'kristy@gmail.com',
    #   'country': 'Spain',
    #   'city': 'Madrid',
    #   'bio': 'My name is Kristy!',
    #   'status': 'In a meeting!'
    # })

    #response = updateClientProfile(request, 'kristy')
    # self.users = User.objects.get(id=1)
    # print(response)
    #self.assertEqual(self.user.status, "My name is Kristy!")
    #self.assertEqual(response.status_code, 302)
    #self.assertRedirects(response, '/profiles/client/kristy/')
    #self.assertEqual(cat.username, 'kristy22')