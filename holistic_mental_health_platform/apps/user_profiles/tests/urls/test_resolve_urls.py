from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_client_profile_url_resolves(self):
    url = reverse('client-profile', args=['kristy'])
    self.assertEquals(resolve(url).func, clientProfile)

  def test_update_client_profile_url_resolves(self):
    url = reverse('edit-client-profile', args=['kristy'])
    self.assertEquals(resolve(url).func, updateClientProfile)

  def test_service_provider_profile_url_resolves(self):
    url = reverse('service-provider-profile', args=['jane_therapist'])
    self.assertEquals(resolve(url).func, serviceProviderProfile)

  def test_update_service_provider_profile_url_resolves(self):
    url = reverse('edit-service-provider-profile', args=['jane_therapist'])
    self.assertEquals(resolve(url).func, updateServiceProviderProfile)

  def test_change_password_url_resolves(self):
    url = reverse('change-password')
    self.assertEquals(resolve(url).func, changePassword)