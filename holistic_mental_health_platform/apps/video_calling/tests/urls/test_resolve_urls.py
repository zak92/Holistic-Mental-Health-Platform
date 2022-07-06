from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_lobby_url_resolves(self):
    url = reverse('lobby')
    self.assertEquals(resolve(url).func, lobby)

  def test_room_url_resolves(self):
    url = reverse('room')
    self.assertEquals(resolve(url).func, conferenceRoom)

  def test_blog_post_url_resolves(self):
    url = reverse('get-token')
    self.assertEquals(resolve(url).func, getToken)

  def test_create_member_url_resolves(self):
    url = reverse('create-member')
    self.assertEquals(resolve(url).func, createMember)

  def test_get_member_url_resolves(self):
    url = reverse('get-member')
    self.assertEquals(resolve(url).func, getMember)

  def test_delete_member_url_resolves(self):
    url = reverse('delete-member')
    self.assertEquals(resolve(url).func, deleteMember)

