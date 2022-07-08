from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class ForumHomeViewTest(TestCase):
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
    self.upload_file = open('static/assets/test_image.jpg', 'rb')
    self.discussion_post = DiscussionForumPost.objects.create(
      author=self.user,
      title='Nutrition for mental health',
      category=Category.objects.create(title='Nutrition'),
      discussion_post='This is the body of the post!',
      )
    self.good_url = reverse('forum-home')
    self.bad_url = '/forum-home/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.discussion_post.delete()

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    response = self.client.get('/forums/')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'discussion_forums/forum_home.html')

  def test_correct_response(self):
    '''Check that correct db responses are rendered'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    # response contains author, title and category of blog article
    self.assertIn(b'jane26', response.content)
    self.assertIn(b'Nutrition for mental health', response.content)
    self.assertIn(b'Nutrition', response.content)
   

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_start_new_discussion_logged_in_users(self):
    '''Start new discussion button available only for logged in users'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertContains(response, 'Start New Discussion</a>')

  def test_start_new_discussion_unavailable_for__logged_out_users(self):
    '''Start new discussion button unavailable for anonymous users'''
    response = self.client.get(self.good_url)
    self.assertNotContains(response, 'Start New Discussion</a>')
    