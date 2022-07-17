from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class CommentSerializerTest(APITestCase):
  
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

    self.comment = Comment.objects.create( 
      author=self.user,
      comment='This is a comment!',
    )
    self.comment.save()

    self.CommentSerializer = CommentSerializer(instance=self.comment)
    
  def tearDown(self):
    self.user.delete()
    self.comment.delete()
    self.client_user.delete()
   

  def test_serializer_has_correct_fields(self):
    '''check if all the necessary fields are correct'''
    data = self.CommentSerializer.data 
    self.assertEqual(set(data.keys()), set( 
      ['author', 'comment', 'flagged']
    ))
    
  
  def test_serializer_has_correct_field_values(self):
    '''check if all the the fields contain correct values'''
    data = self.CommentSerializer.data
    # check if data is correct
    self.assertEqual(data['author'], 'kristy')
    self.assertEqual(data['comment'], 'This is a comment!')
    self.assertEqual(data['flagged'], False)
    