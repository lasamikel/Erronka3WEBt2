from django.shortcuts import render, redirect
from .models import Article
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from . import forms
import base64
import pickle



# Create your views here.

def indexHome(request):
    articles = Article.objects.all().order_by('date')
    context = {
        'articles': articles
    }
    return render(request, 'homepage/index.html', context)

def article_details(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        'article': article
    }
    return render(request, 'homepage/post.html', context)

def about(request):
    return render(request, 'homepage/about.html')

@login_required(login_url="accounts/login")
def share_article(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            #save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:home')
    else:
        form = forms.CreateArticle()
    context = {
        'form':form,
    }
    return render(request, 'homepage/share.html', context)

def search_articles(request):
    try:
        cookie = request.COOKIES.get('search_cookie')
        cookie = pickle.loads(base64.b64decode(cookie))
    except:
        pass
    if request.method == 'POST':  
        query = request.POST.get('query')
        encoded_cookie = base64.b64encode(pickle.dumps(query)) #dumps pickle
        encoded_cookie = encoded_cookie.decode("utf-8")
        sql = f"SELECT * FROM homepage_article;"
        if query: 
            sql = f"SELECT * FROM homepage_article WHERE title LIKE %s OR body LIKE %s;"
            results = Article.objects.raw(sql, params=['%'+ query +'%','%'+ query +'%'])
        else:
            results = Article.objects.raw(sql)
    context = {
        'results':results,
    }
    html = render(request, 'homepage/search.html', context)
    html.set_cookie('search_cookie', encoded_cookie)
    return html

    
    
