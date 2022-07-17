from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class DiscussionForumSerializerTest(APITestCase):
  
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
      id=1,
      author=self.user,
      comment='This is a comment!',
    )
    self.comment.save()

    self.category = Category.objects.create(
        title='Mental Health',
        slug = 'mental-health'
    )
    self.category.save()

    self.discussion_forums = DiscussionForumPost.objects.create(
      author=self.user, 
      title='Title of the discussion', 
      category=self.category,
      discussion_post='This is the body of the post',
      
    )
    self.discussion_forums.save()
    self.discussion_forums.comments.add(self.comment.id)
    self.DiscussionForumSerializer = DiscussionForumSerializer(instance=self.discussion_forums)
    
  def tearDown(self):
    self.user.delete()
    self.category.delete()
    self.comment.delete()
    self.discussion_forums.delete()
    self.client_user.delete()
   

  def test_serializer_has_correct_fields(self):
    '''check if all the necessary fields are correct'''
    data = self.DiscussionForumSerializer.data 
    self.assertEqual(set(data.keys()), set( 
      ['pk', 'author', 'title', 'category', 'discussion_post', 'comments', 'flagged', 'date_created']
    ))
    
  
  def test_serializer_has_correct_field_values(self):
    '''check if all the the fields contain correct values'''
    data = self.DiscussionForumSerializer.data
    # check if data is correct
    self.assertEqual(data['author'], 'kristy')
    self.assertEqual(data['title'], 'Title of the discussion')
    self.assertEqual(data['discussion_post'], 'This is the body of the post')
    self.assertEqual(data['comments'][0]['author'], 'kristy')
    self.assertEqual(data['comments'][0]['comment'], 'This is a comment!')
    self.assertEqual(data['flagged'], False)
    self.assertEqual(data['category']['title'], 'Mental Health')