from unicodedata import category
from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json
from django.core.files.uploadedfile import SimpleUploadedFile

class BlogPostViewTest(TestCase):
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

    self.user_2 = User.objects.create_user(  
      id=2,
      username='tom45',
      password='12test1@1542', 
      email='tommy@example.com',
      country='Spain',
      city='Seville'
    )
    self.user_2.is_client = True
    self.user_2.save()
    self.client_user_2 = Client.objects.create(
      user=self.user_2,
      bio="My name is Tom.",
      status='In a meeting!'
    )
    self.client_user_2.save()


    self.upload_file = open('static/assets/test_image.jpg', 'rb')
    self.blog = Article.objects.create(
      author=self.user,
      title='Nutrition for mental health',
      category=Category.objects.create(title='Nutrition'),
      body='This is the body of the article!',
      thumbnail_image=SimpleUploadedFile(self.upload_file.name, self.upload_file.read())
      )
    self.blog.save()
    
    self.good_url = reverse('blog-post', kwargs={'slug': 'nutrition-for-mental-health'})
    self.bad_url = '/blog-post/'

  def tearDown(self):
    self.user.delete()
    self.user_2.delete()
    self.client_user.delete()
    self.client_user_2.delete()
    self.blog.delete()

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location(self):
    response = self.client.get('/blog/article/nutrition-for-mental-health')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/article.html')

  def test_correct_response(self):
    '''Check that correct db responses are rendered'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    # response contains author, title, body and category of blog article
    self.assertIn(b'jane26', response.content)
    self.assertIn(b'Nutrition for mental health', response.content)
    self.assertIn(b'This is the body of the article!', response.content)
    self.assertIn(b'Nutrition', response.content)

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_delete_and_edit_article_logged_in_author(self):
    '''Delete and edit options available only for the logged in author of the article'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertContains(response, 'Delete</a>')
    self.assertContains(response, 'Edit</a>')

  def test_delete_and_edit_article_unavailable_for_logged_out_author(self):
    '''Delete and edit options not available for logged out author'''
    response = self.client.get(self.good_url)
    self.assertNotContains(response, 'Delete</a>')
    self.assertNotContains(response, 'Edit</a>')

  def test_delete_and_edit_article_unavailable_for_other_logged_in_users(self):
    '''Delete and edit options not available for other logged in users '''
    self.client.login(username='tom45', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertNotContains(response, 'Delete</a>')
    self.assertNotContains(response, 'Edit</a>')
    
  
