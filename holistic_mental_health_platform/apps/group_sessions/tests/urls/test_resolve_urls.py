from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_group_signup_url_resolves(self):
    url = reverse('group-signup')
    self.assertEquals(resolve(url).func, liveSessionsList)

  def test_group_signup_confirmation_url_resolves(self):
    url = reverse('group-signup-confirmation', args=['2'])
    self.assertEquals(resolve(url).func, groupSignUpConfirmation)

  def test_group_session_cancellation_url_resolves(self):
    url = reverse('group-session-cancellation', args=['5'])
    self.assertEquals(resolve(url).func, groupBookingCancellation)

  def test_leave_group_url_resolves(self):
    url = reverse('leave-group', args=['2'])
    self.assertEquals(resolve(url).func, clientLeaveGroup)

  def test_schedule_group_sessions_url_resolves(self):
    url = reverse('schedule-group-sessions', args=['tom'] )
    self.assertEquals(resolve(url).func, scheduleGroupSessions)

  def test_available_group_sessions_url_resolves(self):
    url = reverse('available-group-sessions', args=['jane'] )
    self.assertEquals(resolve(url).func, availableGroupSessions)

  def test_edit_group_sessions_url_resolves(self):
    url = reverse('edit-group-session', args=['14'] )
    self.assertEquals(resolve(url).func, updateGroupSession)

  def test_client_group_sessions_url_resolves(self):
    url = reverse('client-group-sessions', args=['jack22'] )
    self.assertEquals(resolve(url).func, clientGroupSessions)

  def test_group_sessions_category_search_url_resolves(self):
    url = reverse('group-sessions-category-search', args=['mental health'])
    self.assertEquals(resolve(url).func, searchByCategory)

  def test_group_sessions_text_search_url_resolves(self):
    url = reverse('group-sessions-text-search')
    self.assertEquals(resolve(url).func, searchByText)