from django.test import TestCase
import json
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from ...serializers import *

class GroupSessionSerializerTest(APITestCase):
  
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

    self.user_2 = User.objects.create_user(  
      id=2,
      username='tom45',
      password='12test1@1542', 
      email='tommy@example.com',
      country='Spain',
      city='Seville'
    )
    self.user_2.is_service_provider = True
    self.user_2.save()

    self.service_provider = ServiceProvider.objects.create(
      user=self.user_2,
      about="My name is Tom.",
      announcements='In a meeting!'
    )
    self.service_provider.save()

    self.group_booking = GroupBooking.objects.create(
      service_provider=self.user_2,
      group_name='Group 1',
      description='This is group 1.',
      category=Category.objects.create(title='Nutrition'), 
      date='2023-08-15',
      time='14:06:00',
      max_members=20,
      duration=60
      )
    self.group_booking.save()
    self.group_booking.members.add(self.user.id)

    self.GroupSessionSerializer = GroupSessionSerializer(instance=self.group_booking)
    
  def tearDown(self):
    self.user.delete()
    self.user_2.delete()
    self.client_user.delete()
    self.service_provider.delete()
    self.group_booking.delete()
   

  def test_serializer_has_correct_fields(self):
    '''check if all the necessary fields are correct'''
    data = self.GroupSessionSerializer.data 
    self.assertEqual(set(data.keys()), set( 
      [
      'service_provider', 'members', 'group_name', 'description', 
      'category', 'date', 'time', 'max_members', 'duration','cancelled'
      ]
    ))
    
  
  def test_serializer_has_correct_field_values(self):
    '''check if all the the fields contain correct values'''
    data = self.GroupSessionSerializer.data
    # check if data is correct
    self.assertEqual(data['service_provider'], 'tom45')
    self.assertEqual(data['members'][0], 'kristy')
    self.assertEqual(data['group_name'], 'Group 1')
    self.assertEqual(data['description'], 'This is group 1.')
    self.assertEqual(data['category']['title'], 'Nutrition')
    self.assertEqual(data['date'], '2023-08-15')
    self.assertEqual(data['time'], '14:06:00')
    self.assertEqual(data['max_members'], 20)
    self.assertEqual(data['duration'], 60)
    self.assertEqual(data['cancelled'], False)
    