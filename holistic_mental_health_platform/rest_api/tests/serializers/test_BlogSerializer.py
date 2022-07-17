from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *
from django.core.files.uploadedfile import SimpleUploadedFile

class BlogSerializerTest(APITestCase):
  
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

    self.BlogSerializer = BlogSerializer(instance=self.blog)
    
  def tearDown(self):
    self.user.delete()
    self.client_user.delete()
    self.blog.delete()
   

  def test_serializer_has_correct_fields(self):
    '''check if all the necessary fields are correct'''
    data = self.BlogSerializer.data 
    self.assertEqual(set(data.keys()), set( 
      ['pk', 'author', 'title', 'body', 'category', 'date_updated', 'thumbnail_image']
    ))
    
  
  def test_serializer_has_correct_field_values(self):
    '''check if all the the fields contain correct values'''
    data = self.BlogSerializer.data
    # check if data is correct
    self.assertEqual(data['author'], 'kristy')
    self.assertEqual(data['title'], 'Nutrition for mental health')
    self.assertEqual(data['body'], 'This is the body of the article!')
    
    