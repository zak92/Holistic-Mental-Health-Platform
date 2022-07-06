from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_registration_url_resolves(self):
    url = reverse('registration')
    self.assertEquals(resolve(url).func, clientsRegistration)

  def test_application_url_resolves(self):
    url = reverse('application')
    self.assertEquals(resolve(url).func, serviceProviderApplication)

  def test_login_url_resolves(self):
    url = reverse('login')
    self.assertEquals(resolve(url).func, userLogin)

  def test_logout_url_resolves(self):
    url = reverse('logout')
    self.assertEquals(resolve(url).func, userLogout)

