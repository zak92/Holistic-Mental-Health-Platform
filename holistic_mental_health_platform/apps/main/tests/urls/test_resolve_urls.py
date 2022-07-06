from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_home_url_resolves(self):
    url = reverse('home')
    self.assertEquals(resolve(url).func, home)

  def test_service_provider_list_url_resolves(self):
    url = reverse('service-provider-list')
    self.assertEquals(resolve(url).func, serviceProviderList)

