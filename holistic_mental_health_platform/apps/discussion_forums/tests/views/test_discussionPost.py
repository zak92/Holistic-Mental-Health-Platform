from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class DiscussionPostViewTest(TestCase):
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
    
    self.comment = Comment.objects.create(
      id=1,
      author=self.user,
      comment='This is a comment'
    )
    self.comment.save()
  

    self.discussion_post = DiscussionForumPost.objects.create(
      id=1,
      author=self.user,
      title='Nutrition for mental health',
      category=Category.objects.create(title='Nutrition'),
      discussion_post='This is the body of the post!',
      )
    self.discussion_post.save()
    self.discussion_post.comments.add(self.comment.id)
    

    self.good_url = reverse('discussion-post', kwargs={ 'slug': 'nutrition-for-mental-health'})
    self.bad_url = '/discussion-post/nutrition-for-mental-health/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.discussion_post.delete()
    self.comment.delete()

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    response = self.client.get('/forums/discussion-post/nutrition-for-mental-health/')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'discussion_forums/discussion_post.html')

  def test_correct_response(self):
    '''Check that correct db responses are rendered'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    # response contains author, title, body and category of the post
    self.assertIn(b'jane26', response.content)
    self.assertIn(b'Nutrition for mental health', response.content)
    self.assertIn(b'This is the body of the post!', response.content)
    self.assertIn(b'Nutrition', response.content)

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_delete_and_edit_article_logged_in_author(self):
    '''Delete and edit options available only for the logged in author of the post'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertContains(response, 'Delete</a>')
    self.assertContains(response, 'Edit</a>')

  def test_delete_and_edit_post_unavailable_for_logged_out_author(self):
    '''Delete and edit options not available for logged out author'''
    response = self.client.get(self.good_url)
    self.assertNotContains(response, 'Delete</a>')
    self.assertNotContains(response, 'Edit</a>')

  def test_delete_and_edit_post_unavailable_for_other_logged_in_users(self):
    '''Delete and edit options not available for other logged in users (not the creator)'''
    self.client.login(username='tom45', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertNotContains(response, 'Delete</a>')
    self.assertNotContains(response, 'Edit</a>')

  
  def test_flag_discussion_post_POST(self):
    '''Test that the post has been flagged by a logged in user'''
    self.client.login(username='tom26', password='12test1@1542')
    self.discussion_post.flagged = True
    self.discussion_post.save()
    response = self.client.post(self.good_url,  self.discussion_post.__dict__, follow=True)
    self.discussion_post.refresh_from_db()
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'This post has been flagged!')
    # form disappears once post has been flagged
    self.assertNotContains(response, ' <input type="submit" value="Flag" name="flag-discussion-post-form" />')
    self.assertEqual(self.discussion_post.flagged, True)

  def test_flag_comments_POST(self):
    '''Test that the post has been flagged by a logged in user'''
    self.client.login(username='tom26', password='12test1@1542')
    self.comment.flagged = True
    self.comment.save()
    response = self.client.post(self.good_url,  self.comment.__dict__, follow=True)
    self.comment.refresh_from_db()
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'This comment has been flagged!')
    # form disappears once comment has been flagged
    self.assertNotContains(response, ' <input type="submit" value="Flag" name="flag-comment-form" />')
    self.assertEqual(self.comment.flagged, True)

  

  

    

  