from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class DiscussionByIDTest(APITestCase):
  
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
   
    self.good_url = reverse('api-discussion-by-id', kwargs={'pk': 1})
    self.bad_url = '/discussion/100/'
    
  def tearDown(self):
    self.user.delete()
    self.category.delete()
    self.comment.delete()
    self.discussion_forums.delete()
    self.client_user.delete()

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
    self.assertTrue('category' in data['results'][0])
    self.assertTrue('discussion_post' in data['results'][0]) 
    self.assertTrue('comments' in data['results'][0]) 
    self.assertTrue('flagged' in data['results'][0]) 
    self.assertTrue('date_created' in data['results'][0]) 

  def test_endpoint_has_correct_field_values(self):
    response = self.client.get(self.good_url, format='json')
    response.render() 
    # check if data is correct
    data = json.loads(response.content)
    self.assertEqual(data['results'][0]['author'], 'kristy')
    self.assertEqual(data['results'][0]['title'], 'Title of the discussion')
    self.assertEqual(data['results'][0]['category']['title'], 'Mental Health')
    self.assertEqual(data['results'][0]['discussion_post'],  'This is the body of the post')
    self.assertEqual(data['results'][0]['comments'][0]['author'], 'kristy')
    self.assertEqual(data['results'][0]['comments'][0]['comment'], 'This is a comment!')
    self.assertEqual(data['results'][0]['flagged'], False)

     