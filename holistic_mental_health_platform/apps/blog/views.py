from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='/accounts/login')
def createBlogPost(request):

  form = CreateArticleForm(initial = {'category': 1 })
  if request.method == 'POST': # if user sent info
    form = CreateArticleForm(request.POST,  request.FILES)  # populated with the data that the user sent
    if form.is_valid(): # validate the data
      instance = form.save(commit=False)
      instance.author = request.user
      instance.save()
      return redirect('blog-home')

  context = {'form':form}
  return render(request, 'blog/create_blog_post.html', context)

def blogHome(request):
  articles = Article.objects.all()
  categories = Category.objects.all()
  context = {'articles': articles, 'categories': categories}
  return render(request, 'blog/blog_home.html', context)

def blogPost(request, slug):
  article = Article.objects.get(slug=slug)
  categories = Category.objects.all() 
  context = {'article': article, 'categories': categories}
  return render(request, 'blog/article.html', context)

def searchByCategory(request, slug):
  # get post with unique slug
  categories = Category.objects.all() 
  category = get_object_or_404(Category, slug=slug)

  article_list = Article.objects.filter(category=category)

  context = {
    'categories': categories,
    'category': category,
    'article_list':article_list
  }
  return render(request, 'blog/category_search_results.html', context)

def searchByText(request):
  
  categories = Category.objects.all()
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  # Search for groups
  article_list = Article.objects.filter(
     Q(title__icontains=q) |                                                                              
     Q(body__icontains=q)
    ) 
  
  

  context = {
    'article_list':article_list,
    'categories': categories,

  }
  return render(request, 'blog/text_search_results.html', context)


def deleteBlogPost(request, pk):
  article = Article.objects.get(id=pk)
  if request.user != article.author:  # if user is not the creator of message - they cannot delete it
   return redirect('blog-home')
  if request.method == 'POST':
    article.delete()
    return redirect('blog-home')
  return render(request, 'blog/delete.html', {'article': article})


def updateBlogPost(request, pk):
  article = Article.objects.get(id=pk)
  form = CreateArticleForm(instance=article) # the form will be pre-filled with data
  if request.user != article.author:  # if user is not the creator - they cannot update it
    return redirect('blog-home')
  if request.method == 'POST': # if user sent info
    form = CreateArticleForm(request.POST, request.FILES, instance=article)  # populated with the data that the user sent - update a group, do not create a new one
    if form.is_valid(): # validate the data
      form.save()
      return redirect('blog-home')
  context = {'form': form, 'article': article}
  return render(request, 'blog/create_blog_post.html', context)