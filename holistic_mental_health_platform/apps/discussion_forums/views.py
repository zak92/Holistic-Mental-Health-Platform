from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
# https://github.com/SelmiAbderrahim/Django-Community-Forum-Website/tree/main/main
def forumHome(request):
  categories = Category.objects.all()
  discussion_list = DiscussionForumPost.objects.all()
  
  context = {
    'discussion_list': discussion_list,
    'categories': categories,
   
  }

  return render(request, 'discussion_forums/forum_home.html', context)


def discussionPost(request, slug):
  # get post with unique slug
  categories = Category.objects.all()
  post = get_object_or_404(DiscussionForumPost, slug=slug)

  if "comment-form" in request.POST:
    if request.user.is_authenticated:
      comment = request.POST.get("comment")
      new_comment, created = Comment.objects.get_or_create(author=request.user, comment=comment)
      post.comments.add(new_comment.id)
      return redirect('discussion-post', slug)
    else: 
      return redirect('login')
  

  flag_discussion_post_form = FlagDiscussionPostForm(instance=post)
  if "flag-discussion-post-form" in request.POST:
    if request.user.is_authenticated:
      flag_discussion_post_form = FlagDiscussionPostForm(request.POST, instance=post)
      if flag_discussion_post_form.is_valid():
        flag_discussion = flag_discussion_post_form.save()
        flag_discussion.save()
        return redirect('discussion-post', slug)
    else: 
      return redirect('login')


  if "flag-comment-form" in request.POST:
    if request.user.is_authenticated:
      comment_id = Comment.objects.get(pk=request.POST.get('comment_id'))
      comment_id.flagged = True
      comment_id.save()
      return redirect('discussion-post', slug)
    else: 
      return redirect('login')
   
  
  context = { 'post': post, 'categories': categories,
              'flag_discussion_post_form':flag_discussion_post_form,

            } 
  return render(request, 'discussion_forums/discussion_post.html', context)

@login_required(login_url='/accounts/login')
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

def deleteDiscussionPost(request, pk):
  post = DiscussionForumPost.objects.get(id=pk)
  if request.user != post.author:  # if user is not the creator of message - they cannot delete it
    return redirect('forum-home')
  if request.method == 'POST':
    post.delete()
    return redirect('forum-home')

  context = {'post': post, 'type': 'discussion post'}
  return render(request, 'discussion_forums/delete.html', context )


def updateDiscussionPost(request, pk):
  post = DiscussionForumPost.objects.get(id=pk)
  create_discussion_post_form = CreateDiscussionPostForm(instance=post) # the form will be pre-filled with data
  if request.user != post.author:  # if user is not the creator - they cannot update it
    return redirect('forum-home')
  if request.method == 'POST': # if user sent info
    create_discussion_post_form = CreateDiscussionPostForm(request.POST, instance=post)  # populated with the data that the user sent - update a group, do not create a new one
    if create_discussion_post_form.is_valid(): # validate the data
      create_discussion_post_form.save()
      return redirect('forum-home')
  context = {'create_discussion_post_form': create_discussion_post_form, 'post':post}
  return render(request, 'discussion_forums/create_discussion_post.html', context)



def deleteComment(request, pk):
  comment = Comment.objects.get(id=pk)
  
  if request.user != comment.author:  # if user is not the creator of message - they cannot delete it
    return redirect('forum-home')
  if request.method == 'POST':
    comment.delete()
    return redirect('forum-home')
    
  context = {'comment': comment, 'type': 'comment'}
  return render(request, 'discussion_forums/delete.html', context )