from unicodedata import category
from urllib import response
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ...views import *  
import json
from django.core.files.uploadedfile import SimpleUploadedFile

class DeleteBlogPostViewTest(TestCase):
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
      author=self.user,
      title='Nutrition for mental health',
      category=Category.objects.create(title='Nutrition'),
      body='This is the body of the article!',
      thumbnail_image=SimpleUploadedFile(self.upload_file.name, self.upload_file.read())
      )
    self.blog.save()

    self.good_url = reverse('delete-blog-post', kwargs={ 'pk': '1'})
    self.bad_url = '/delete-blog-post/'

  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.blog.delete()

  def test_url_accessible_by_name_logged_in_author(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url)
    self.assertEqual(response.status_code, 200)

  def test_url_exists_at_location_logged_in_author(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get('/blog/delete-blog-post/1/')
    self.assertEqual(response.status_code, 200)

  def test_delete_unavailable_for_all_logged_out_users(self):
    '''Delete not available for all logged out users'''
    response = self.client.get(self.good_url)
    # users get redirected to blog home page - code 302
    self.assertEqual(response.status_code, 302)

  def test_delete_unavailable_for_other_logged_in_users(self):
    '''Delete not available for other logged in users (not the author)'''
    self.client.login(username='tom45', password='12test1@1542')
    response = self.client.get(self.good_url)
    # users get redirected to blog home page - code 302
    self.assertEqual(response.status_code, 302)

  def test_uses_correct_template_logged_in_author(self):
    '''Test that the correct template is used for logged in author'''
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.get(self.good_url, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/delete.html')

  def test_delete_blog_post_POST(self):
    self.client.login(username='jane26', password='12test1@1542')
    response = self.client.delete(self.good_url, follow=True)
    self.assertEqual(response.status_code, 200)

  