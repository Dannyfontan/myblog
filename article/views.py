import markdown

from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Article
from . forms import ArticleForm
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
        ).order_by('-created')
    else:
        search = ''
        article_list = Article.objects.all().order_by('-created')

    paginator = Paginator(article_list, 3)
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

def article_create(request):
    if request.method == "POST":
        article_form = ArticleForm(data=request.POST)
        if(article_form.is_valid()):
            new_article = article_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误")
    #返回空表单供填写
    else:
        article_form = ArticleForm()
        context = {'article_form' : article_form}
        return render(request, 'article/create.html', context)

def article_safe_delete(request, id):
    if request.method == "POST":
        article = Article.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("非法请求")

def article_update(request, id):
    # 获取需要修改的具体文章对象
    article = Article.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_form = ArticleForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_form': article_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)