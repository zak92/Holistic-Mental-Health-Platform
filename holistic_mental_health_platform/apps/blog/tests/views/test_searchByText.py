from unicodedata import category
from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
from django.db.models import Q
from django.core.files.uploadedfile import SimpleUploadedFile

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
      bio="My name is Jane.",
      status='Busy!'
    )
    self.client_user.save()
    self.upload_file = open('static/assets/test_image.jpg', 'rb')
    self.blog = Article.objects.create(
      id=1,
      author=self.user,
      title='Importance of mental health',
      category=Category.objects.create(title='Mental Health'),
      body='This is the body of the article!',
      thumbnail_image=SimpleUploadedFile(self.upload_file.name, self.upload_file.read())
      )
    self.blog.save()
    
    self.good_url = reverse('blog-text-search')
    self.bad_url = '/blog-text-search/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.blog.delete()

  def test_url_accessible_by_name(self):
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
  
  def test_url_exists_at_location(self):
    response = self.client.get('/blog/blog-text-search')
    self.assertEqual(response.status_code, 200)

  def test_uses_correct_template(self):
    '''Test that the correct template is used'''
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/text_search_results.html')

  def test_correct_response(self):
    '''Check that correct db responses are rendered'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    # response contains author, title and category of blog article
    self.assertIn(b'jane26', response.content)
    self.assertIn(b'Importance of mental health', response.content)
    self.assertIn(b'Mental Health', response.content)

  def test_fail_bad_url(self):
    '''Test fails on incorrect url'''
    response = self.client.get(self.bad_url, format='json')
    self.assertEqual(response.status_code, 404)

  def test_search_function(self):
    '''Test if the search function gives the correct results'''
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)
    article_list = Article.objects.filter(
     Q(title__icontains='mental health') |                                                                              
     Q(body__icontains='mental health')
    ) 
    self.assertEqual(article_list[0].id, 1)
    self.assertEqual(article_list[0].title, 'Importance of mental health')
