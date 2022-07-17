from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *
from django.core.files.uploadedfile import SimpleUploadedFile

class BlogByCategoryTest(APITestCase):
  
  def setUp(self):
    self.user = User.objects.create_user( 
      id=1,
      username='kristy',
      password='12test12', 
      email='test@example.com',
      country='',
      city='Madrid'
    )
    self.user.is_client = True
    self.user.save()
    self.client_user = Client.objects.create(
      user=self.user,
      bio="My name is Kristy",
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

    self.good_url = reverse('api-blog-by-category', kwargs={'category': 'nutrition'})
    self.bad_url = '/blog-by-category/nutrition'
    
  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.blog.delete()
   
  def test_endpoint_accessible_on_good_url(self):
    '''test for 200 response code for user endpoint'''
    response = self.client.get(self.good_url)
    # test if the http code is 404
    self.assertEqual(response.status_code, 200)

  def test_fail_on_bad_url(self):
    '''test for 404 response code for user endpoint'''
    response = self.client.get(self.bad_url)
    # test if the http code is 404
    self.assertEqual(response.status_code, 404)

  def test_endpoint_has_correct_field(self):
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertTrue('author' in data['results'][0])
    self.assertTrue('title' in data['results'][0])
    self.assertTrue('body' in data['results'][0])
    self.assertTrue('category' in data['results'][0]) 
    self.assertTrue('date_updated' in data['results'][0]) 
    self.assertTrue('thumbnail_image' in data['results'][0]) 
    

  def test_endpoint_has_correct_field_values(self):
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertEqual(data['results'][0]['author'], 'kristy')
    self.assertEqual(data['results'][0]['title'], 'Nutrition for mental health')
    self.assertEqual(data['results'][0]['body'], 'This is the body of the article!')
    self.assertEqual(data['results'][0]['category']['title'], 'Nutrition')