from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/client')
def createBlogPost(request):
  form = CreateArticle()
  if request.method == 'POST': # if user sent info
    form = CreateArticle(request.POST,  request.FILES)  # populated with the data that the user sent
    if form.is_valid(): # validate the data
      instance = form.save(commit=False)
      instance.author = request.user
      instance.save()
      return redirect('articleList')

  context = {'form':form}
  return render(request, 'blog/create-blog-post.html', context)

def articleList(request):
  articles = Article.objects.all().order_by('date_created')
  context = {'articles': articles}
  return render(request, 'blog/article-list.html', context)

def blogPost(request, slug):
  article = Article.objects.get(slug=slug)
  context = {'article': article}
  return render(request, 'blog/article.html', context)
