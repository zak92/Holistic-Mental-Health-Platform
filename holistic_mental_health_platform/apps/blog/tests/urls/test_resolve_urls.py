from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_create_blog_post_url_resolves(self):
    url = reverse('create-blog-post')
    self.assertEquals(resolve(url).func, createBlogPost)

  def test_blog_home_url_resolves(self):
    url = reverse('blog-home')
    self.assertEquals(resolve(url).func, blogHome)

  def test_blog_post_url_resolves(self):
    url = reverse('blog-post', args=['nutrition'])
    self.assertEquals(resolve(url).func, blogPost)

  def test_blog_category_search_url_resolves(self):
    url = reverse('blog-category-search', args=['mental health'])
    self.assertEquals(resolve(url).func, searchByCategory)

  def test_blog_text_search_url_resolves(self):
    url = reverse('blog-text-search')
    self.assertEquals(resolve(url).func, searchByText)

  def test_delete_blog_post_url_resolves(self):
    url = reverse('delete-blog-post', args=['2'])
    self.assertEquals(resolve(url).func, deleteBlogPost)

  def test_update_blog_post_url_resolves(self):
    url = reverse('update-blog-post', args=['2'] )
    self.assertEquals(resolve(url).func, updateBlogPost)