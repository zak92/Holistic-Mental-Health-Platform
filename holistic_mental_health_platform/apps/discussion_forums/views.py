from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
# https://github.com/SelmiAbderrahim/Django-Community-Forum-Website/tree/main/main
def forumHome(request):
  categories = Category.objects.all()
  #category = get_object_or_404(Category, slug=slug)
  #discussion_list_by_category = DiscussionForumPost.objects.filter(category=category)
  discussion_list = DiscussionForumPost.objects.all()
  
  context = {
    'discussion_list': discussion_list,
    'categories': categories,
    #'discussion_list_by_category': discussion_list_by_category
  }

  return render(request, 'discussion_forums/forum_home.html', context)


def discussionPost(request, slug):
  # get post with unique slug
  categories = Category.objects.all()
  post = get_object_or_404(DiscussionForumPost, slug=slug)

  if "comment-form" in request.POST:
      comment = request.POST.get("comment")
      new_comment, created = Comment.objects.get_or_create(author=request.user, comment=comment)
      post.comments.add(new_comment.id)

      return redirect('discussion-post', slug)


  


  # sp_booking_form = CancelBookingForm(instance=post)
  # if request.method == 'POST': # if user sent info
  #   sp_booking_form = CancelBookingForm(request.POST, instance=booking)
  #   if sp_booking_form.is_valid():
  #     sp_book = sp_booking_form.save()
  #     sp_book.save()
  #     return redirect('service-provider-profile', booking.service_provider)
      
  
  context = { 'post': post, 'categories': categories,}
  return render(request, 'discussion_forums/discussion_post.html', context)


def createDiscussionPost(request):
  create_discussion_post_form = CreateDiscussionPostForm(initial = {'category': 1 })

  if request.method == 'POST': # if user sent info
    create_discussion_post_form = CreateDiscussionPostForm(request.POST)
    if create_discussion_post_form.is_valid():
      post = create_discussion_post_form.save(commit=False)
      post.author = request.user
      post.save()

      return redirect('forum-home')
  context = {
    'create_discussion_post_form': create_discussion_post_form
  }
  return render(request, 'discussion_forums/create_discussion_post.html', context)


def searchByCategory(request, slug):
  # get post with unique slug
  categories = Category.objects.all()
  category = get_object_or_404(Category, slug=slug)
  #discussion_list_by_category = DiscussionForumPost.objects.filter(category=category)
  #discussion_list = DiscussionForumPost.objects.all().order_by('date_updated')
  discussion_list = DiscussionForumPost.objects.filter(category=category)

  context = {
    'discussion_list': discussion_list,
    'categories': categories,
    'category': category
    #'discussion_list_by_category': discussion_list_by_category
  }
  return render(request, 'discussion_forums/category_search_results.html', context)


def searchByText(request):
  # get post with unique slug
  categories = Category.objects.all()
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  # Search for groups
  discussion_list = DiscussionForumPost.objects.filter(
     Q(title__icontains=q) |                                                                              
     Q(discussion_post__icontains=q)
    ) 
  
  

  context = {
    'discussion_list':discussion_list,
    'categories': categories,

  }
  return render(request, 'discussion_forums/text_search_results.html', context)