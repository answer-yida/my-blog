from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View

from . import models
import markdown
#引入分页模块
from django.core.paginator import Paginator
from django.http import HttpResponse
#引入定义的表单类
from .forms import ArticlePostForm
#引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#引入Q对象
from django.db.models import Q
from comment.models import Comment
from .models import ArticleColumn
from comment.forms import CommentForm
from django.shortcuts import get_object_or_404
# Create your views here.
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    #初始化查询集
    article_list = models.ArticlePost.objects.all()
    #用户搜索逻辑
    if search:
       article_list = models.ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
            )
    else:
        #将search参数值为空
        search = ''
    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
        # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    #每页显示3篇文章
    paginator = Paginator(article_list,3)
    #获取url的页码
    page = request.GET.get('page')
    #将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    #需要传递给模板的对象
    context = {'articles':articles,
               'order':order,
               'search':search,
               'column': column,
               'tag': tag,
               }
    # return HttpResponse('hello world')
    return render(request, 'article/list.html', context)

def article_detail(request,id):

    #取出文章

    # article = models.ArticlePost.objects.get(id=id)
    article = get_object_or_404(models.ArticlePost, id=id)
    #取出文章评论

    comments = Comment.objects.filter(article=id)
    #浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            #目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    #载入模板  并返回context对象给浏览器渲染
    # 需要传递给模板的对象
    context = { 'article': article, 'toc': md.toc, 'comments': comments,
                'comment_form':comment_form,
                }
    return  render(request,'article/detail.html',context)

#写文章的视图
#检查登录
@login_required(login_url='/userprofile/login/')
def article_create(request):
    #post请求
    if request.method == "POST":
        #将提交的数据复制到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        #判断是否满足要求
        if article_post_form.is_valid():
            #保存数据，但是暂时不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            #新文章保存到数据库中
            new_article.save()
            article_post_form.save_m2m()
            #完成后返回文章列表
            return redirect('article:article_list')
        #数据不合法
        else:
            return HttpResponse('表单内容有误请重新书写')
    #get请求
    else:
        #创建表单实例
        article_post_form = ArticlePostForm
        columns = ArticleColumn.objects.all()
        #幅值上下文
        context = {'article_post_form':article_post_form,'columns':columns}
        return render(request,'article/create.html',context)


#删除文章
def article_delete(request,id):
    #获取要删除的文章id
    article = models.ArticlePost.objects.get(id=id)
    #删除文章
    article.delete()
    #返回文章列表
    return redirect('article:article_list')
@login_required(login_url='userprofile/login/')
def article_safe_delete(request,id):
    if request.method=='POST':
        article = models.ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权删除这篇文章")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

#提醒用户登录

@login_required(login_url='userprofile/login/')
def article_update(request,id):
    '''
    更新文章视图函数
    通过post方法提交表单，更新title，boby字段
    GEt方法进入初始表单页面
    id：文章的 id
    '''
    #获取需要修改的具体文章对象
    article= models.ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章")
    #post请求
    if request.method=="POST":
        #将提交的数据复制到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        #判断是否满足要求
        if article_post_form.is_valid():
            #保存到数据库
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] !='none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            #完成后返回文章
            return redirect("article:article_detail",id=id)
        #不符合要求
        else:
            return HttpResponse("表单内容不符合要求")
    #get请求
    else:
        #创建表单实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        return render(request,'article/update.html',context)

# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = models.ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')

