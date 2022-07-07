from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from ...views import * 

class TestForms(TestCase):

  def test_create_discussion_post_form_is_valid(self):
    ''' Check if form is valid '''
    Category.objects.create(title='Mental Health')
    data = {
      'title': 'Mental Health',
      'discussion_post': 'lorem ipsum init',
      'category':  Category.objects.get(title='Mental Health'),
      }
    form = CreateDiscussionPostForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())

  def test_create_discussion_post_form_no_data(self):
    ''' Check if form is not valid if no data is submitted'''
    data = {}
    form = CreateDiscussionPostForm(data)
    # check if the form is not valid
    self.assertFalse(form.is_valid())
     # check that the total errors is 3
    self.assertEquals(len(form.errors), 3)
    
  def test_flag_discussion_post_form_is_valid(self):
    ''' Check if form is valid '''
    data = {
      'flagged': True,
      }
    form = FlagDiscussionPostForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())


    # 4 extra forms to test

