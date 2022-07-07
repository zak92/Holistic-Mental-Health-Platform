from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from ...views import * 

class TestForms(TestCase):
  def test_group_booking_form_is_valid(self):
    ''' Check if form is valid '''
    Category.objects.create(title='Mental Health')
    data = {
      'group_name': 'Group 1',
      'description': 'lorem ipsum init',
      'category':  Category.objects.get(title='Mental Health'),
      'date': 'July 17, 2022',
      'time': '14:06:00',
      'duration': 60,
      'max_members': 20

      }
    form = GroupBookingForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())

  def test_group_booking_form_no_data(self):
    ''' Check if form is not valid if no data is submitted'''
    data = {}
    form = GroupBookingForm(data)
    # check if the form is not valid
    self.assertFalse(form.is_valid())
     # check that the total errors is 7
    self.assertEquals(len(form.errors), 7)
   
  def test_cancel_group_booking_form_is_valid(self):
    ''' Check if form is valid '''
    data = {
      'cancelled': True
      }
    form = CancelGroupBookingForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())