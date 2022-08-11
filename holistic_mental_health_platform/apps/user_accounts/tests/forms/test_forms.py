from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from ...views import * 



class TestForms(TestCase):
  
  def test_client_user_creation_form_is_valid(self):
    form =  ClientUserCreationForm(data={
      'username': 'user',
      'email': "user@mp.com", 
      'password1': "urt@hello123", 
      'password2': "urt@hello123",
      'agree': 'True'
    
      })
    # check that the form is valid
    self.assertTrue(form.is_valid())

  def test_client_user_creation_form_no_data(self):
    form = ClientUserCreationForm(data={})
    # check that the empty form is not validated
    self.assertFalse(form.is_valid())


  def test_client_user_creation_form_errors(self):
    form = ClientUserCreationForm(data={})
    # check that the empty form is not validated
    self.assertFalse(form.is_valid())
    # check that the total errors is 5
    self.assertEquals(len(form.errors), 5)


  def test_service_provider_apply_form_is_not_valid(self):
    form = ServiceProviderRegistrationApplicationForm(data={})
    # check that the form is valid
    self.assertFalse(form.is_valid())
    # check that the total errors is 2
    self.assertEquals(len(form.errors), 3)