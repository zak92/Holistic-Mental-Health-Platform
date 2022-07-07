
from django.test import SimpleTestCase, TestCase, RequestFactory
from django.urls import reverse, resolve
from ...views import * 
from django.core.files.uploadedfile import SimpleUploadedFile

class TestCreateArticleForm(TestCase):

  def test_create_article_form_is_valid(self):
    ''' Check if form is valid '''
    Category.objects.create(title='Nutrition')
    upload_file = open('static/assets/test_image.jpg', 'rb')
    data = {
      'title': 'Nutrition',
      'category': Category.objects.get(title='Nutrition'),
      'body': 'This is the body of the article!'
    }
    file_dict = {'thumbnail_image': SimpleUploadedFile(upload_file.name, upload_file.read())}
    
    form = CreateArticleForm(data,  file_dict)
    # check if the form is valid
    self.assertTrue(form.is_valid())
    
  def test_create_article_no_data(self):
    ''' Check if empty form is not valid '''
    form = CreateArticleForm(data={})
    # check that the empty form is not valid
    self.assertFalse(form.is_valid())
    # check that the total errors is 4
    self.assertEquals(len(form.errors), 4)
  
   