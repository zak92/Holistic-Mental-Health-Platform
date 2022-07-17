from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *


class CategorySerializerTest(APITestCase):
  
  def setUp(self):

    self.category = Category.objects.create(
        title='Mental Health',
        slug = 'mental-health'
    )

    self.category.save()
    
    self.CategorySerializer = CategorySerializer(instance=self.category)
    
  def tearDown(self):
    self.category.delete()
   

  def test_serializer_has_correct_fields(self):
    '''check if all the necessary fields are correct'''
    data = self.CategorySerializer.data 
    self.assertEqual(set(data.keys()), set( 
       ['title','slug']
    ))
    
  
  def test_serializer_has_correct_field_values(self):
    '''check if all the the fields contain correct values'''
    data = self.CategorySerializer.data
    # check if data is correct
    self.assertEqual(data['title'], 'Mental Health')
    self.assertEqual(data['slug'], 'mental-health')
   
    
    