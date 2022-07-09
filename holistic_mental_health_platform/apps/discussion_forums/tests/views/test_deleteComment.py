from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json

class DeleteCommentViewTest(TestCase):
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
    

    self.good_url = reverse('delete-comment', kwargs={ 'pk': '1'})
    self.bad_url = '/delete-comment/1/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.discussion_post.delete()
    self.comment.delete()

  def test_url_accessible_by_name_only_for_logged_in_users(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location_only_for_logged_in_users(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get('/forums/delete-comment/1/')
    self.assertEqual(response.status_code, 200)
  
  def test_url_inaccessible_at_for_anonymous_users(self):
    '''Anonymous users cannot access the page'''
    response = self.client.get('/forums/delete-comment/1/')
    self.assertNotEqual(response.status_code, 200)

  def test_delete_unavailable_for_all_logged_out_users(self):
    '''Delete not available for all logged out users'''
    response = self.client.get(self.good_url)
    # users get redirected to forum home page - code 302
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('forum-home'))

  def test_delete_unavailable_for_other_logged_in_users(self):
    '''Delete not available for other logged in users (not the author)'''
    self.client.login(username='tom45', password='12test1@1542')
    response = self.client.get(self.good_url)
    # users get redirected to forum home page - code 302
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('forum-home'))
  
  def test_uses_correct_template_logged_in_user(self):
    '''Test that the correct template is used for logged in user (author of the comment)'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'discussion_forums/delete.html')

  def test_delete_comment_post_POST(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.delete(self.good_url, follow=True)
    self.assertEqual(response.status_code, 200)
