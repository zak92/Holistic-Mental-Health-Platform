from django.test import SimpleTestCase, TestCase, RequestFactory
from django.urls import reverse, resolve
from ...views import * 


class TestForms(TestCase):

  def test_booking_form_is_valid(self):
    ''' Check if form is valid '''
    data = {
      'date': 'July 17, 2022',
      'time': '14:06:00'
      }
    form = BookingForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())

  def test_booking_form_no_data(self):
    ''' Check if form is not valid '''
    data = {}
    form = BookingForm(data)
    # check if the form is not valid
    self.assertFalse(form.is_valid())
     # check that the total errors is 2
    self.assertEquals(len(form.errors), 2)

  def test_client_booking_form_is_valid(self):
    ''' Check if form is valid '''
    data = {'booked': True}
    form = ClientBookingForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())

  def test_client_cancel_booking_form_is_valid(self):
    ''' Check if form is valid '''
    data = {'cancelled': True}
    form = ClientCancelBookingForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())

  def test_confirm_booking_form_is_valid(self):
    ''' Check if form is valid '''
    data = {'confirmed': True}
    form = ConfirmBookingForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())

  def test_cancel_booking_form_is_valid(self):
    data = {'cancelled': True}
    form = CancelBookingForm(data)
    # check if the form is valid
    self.assertTrue(form.is_valid())



  