from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json


class UpdatePostViewTest(TestCase):
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
      bio="My name is Jane.",
      status='Busy!'
    )
    self.client_user.save()
   
    self.discussion_post = DiscussionForumPost.objects.create(
      author=self.user,
      title='Nutrition for mental health',
      category=Category.objects.create(title='Nutrition'),
      discussion_post='This is the body of the post!',
      )
    self.good_url = reverse('update-discussion-post', kwargs={ 'pk': 1})
    self.bad_url = '/update-discussion-post/1/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.discussion_post.delete()

  def test_url_accessible_by_name_logged_in_author(self):
    '''Only the logged in post creator can access this page'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
  
    
  def test_url_exists_at_location_logged_in_author(self):
    '''Only the logged in post creator can access this page'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get('/forums/update-discussion-post/1/')
    self.assertEqual(response.status_code, 200)

  def test_update_unavailable_for_all_logged_out_users(self):
    '''Update post not available for all logged out users'''
    response = self.client.get(self.good_url)
    # users get redirected to forum home page - code 302
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/forums/')


  def test_uses_correct_template_logged_in_author(self):
    '''Test that the correct template is used for logged in post creator'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'discussion_forums/create_discussion_post.html')

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_update_discussion_post_POST(self):
    '''Test that the title has been updated by logged in post creator'''
    self.client.login(username='jane26', password='12test1@1542')
    self.discussion_post.title = 'Importance of mental health'
    self.discussion_post.save()
    response = self.client.post(self.good_url,  self.discussion_post.__dict__, follow=True)
    self.discussion_post.refresh_from_db()
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Importance of mental health')
    self.assertNotContains(response, 'Nutrition for mental health')
    self.assertEqual(str(self.discussion_post.title),  'Importance of mental health')