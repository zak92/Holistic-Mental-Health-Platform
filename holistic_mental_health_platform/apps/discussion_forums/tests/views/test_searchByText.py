from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json
from django.db.models import Q

class SearchByTextViewTest(TestCase):
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
    self.discussion_post = DiscussionForumPost.objects.create(
      id=1,
      author=self.user,
      title='Nutrition for mental health',
      category=Category.objects.create(title='Nutrition'),
      discussion_post='This is the body of the post!',
      )
    self.good_url = reverse('discussion-post-text-search')
    self.bad_url = '/discussion-post-text-search/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.discussion_post.delete()

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    response = self.client.get('/forums/discussion-post-text-search')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'discussion_forums/text_search_results.html')

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

  def test_search_function(self):
    '''Test if the search function gives the correct results'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    discussion_list = DiscussionForumPost.objects.filter(
     Q(title__icontains='nutrition') |                                                                              
     Q(discussion_post__icontains='nutrition')
    ) 
    self.assertEqual(discussion_list[0].id, 1)
    self.assertEqual(discussion_list[0].title, 'Nutrition for mental health')
