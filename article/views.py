import markdown

from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Article
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.html import strip_tags

# Create your views here.
def article_list(request):
    search = request.GET.get('search')

    if search:
        article_list = Article.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        ).order_by('-updated')
    else:
        search = ''
        article_list = Article.objects.all().order_by('-updated')

    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ])
    for article in articles:
        article.body = strip_tags(md.convert(article.body))
    
    context = {'articles': articles, 'search': search}
    return render(request, 'article/list.html', context)

def article_detail(request, id):
    article = Article.objects.get(id=id)
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    context = {'article': article, 'toc': md.toc}
    return render(request, 'article/detail.html', context)

def article_columnlist(request):
    column_name = request.GET.get('column')

    if column_name:
        column_list = Article.objects.filter(title=column_name)
        
    else:
        column_name = ""
        column_list = ""

    context = {'column_list' : column_list}
    return render(request, 'article/columnlist.html', context)