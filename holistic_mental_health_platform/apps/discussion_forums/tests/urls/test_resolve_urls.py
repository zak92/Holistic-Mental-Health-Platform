from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_forum_home_url_resolves(self):
    url = reverse('forum-home')
    self.assertEquals(resolve(url).func, forumHome)

  def test_discussion_post_url_resolves(self):
    url = reverse('discussion-post',  args=['Mind and Health'])
    self.assertEquals(resolve(url).func, discussionPost)

  def test_discussion_post_category_search_url_resolves(self):
    url = reverse('discussion-post-category-search', args=['Nutrition'])
    self.assertEquals(resolve(url).func, searchByCategory)

  def test_discussion_post_text_search_url_resolves(self):
    url = reverse('discussion-post-text-search')
    self.assertEquals(resolve(url).func, searchByText)

  def test_create_discussion_post_url_resolves(self):
    url = reverse('create-discussion-post')
    self.assertEquals(resolve(url).func, createDiscussionPost)

  def test_delete_discussion_post_url_resolves(self):
    url = reverse('delete-discussion-post', args=['2'])
    self.assertEquals(resolve(url).func, deleteDiscussionPost)

  def test_update_discussion_post_url_resolves(self):
    url = reverse('update-discussion-post', args=['2'] )
    self.assertEquals(resolve(url).func, updateDiscussionPost)

  def test_delete_comment_url_resolves(self):
    url = reverse('delete-comment', args=['3'] )
    self.assertEquals(resolve(url).func, deleteComment)