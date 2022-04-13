from distutils.command.build_scripts import first_line_re
from hashlib import new
from re import I
#from turtle import title, update
from django.forms import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.test import tag
from markupsafe import re
#from numpy import identity
# 导入数据模型ArticlePost
from .models import ArticlePost, ArticleColumn
# 倒入支持markdown
import markdown
# redirect重定向模块
from django.shortcuts import redirect
# 引入刚才定义的ArticlePostForm表单类
from .forms import  ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 引入分页模块
from django.core.paginator import Paginator
# 引入Q对象
from django.db.models import Q
# 引入评论对象
from comment.models import Comment
from comment.forms import CommentForm



def article_list(request):

    search = request.GET.get('search')
    order = request.GET.get('order')
    column_id = request.GET.get('column_id')
    tag = request.GET.get('tag')

    article_list = ArticlePost.objects.all()
    # article_list = ArticlePost.objects.raw('select * from article_articlepost a left join article_tag b on  a.id = b.article_id')
    # 如果有过滤查询
    if search:
        # 根据GET请求中查询条件
        # 返回不同排序列表的对象数组
        if order == 'total_view':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_view')

        else:
            # 取出所有博客文章
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将search变量设为空
        search = ''
        if order == 'total_view':
            article_list = ArticlePost.objects.all().order_by('-total_view')
        if column_id and column_id != 'None':
            article_list = ArticlePost.objects.filter(column_id=column_id)
        if tag and tag != 'None':
            # article_list = ArticlePost.objects.filter(id__in=Article_tag.objects.values('article_id').filter(tag__icontains=tag))
            # article_list = ArticlePost.objects.raw('select * from article_articlepost a left join article_tag b on  a.id = b.article_id where tag=%s',[tag])
            article_list = article_list.filter(tags__icontains=tag)
        # else:
        #     tags = Article_tag.objects.all()
        #     order = ''
        #     column_id = ''
        #     article_list = ArticlePost.objects.all()
            # 将column_id 设置为空 
            
    # 每个page显示s三篇article
    paginator = Paginator(article_list, 3)
    # 从request的参数中获取到当前要请求的page页,如果没有为none
    page = request.GET.get('page')
    # 把对应的page页中的信息反给前端，如果为none返回第一个page
    articles = paginator.get_page(page)
    # 需要传递给模版(template)的对象
    context = {
        'articles': articles,
        }

    # render函数：载入模块，并返回context对象
    return render(request, 'article/list.html', locals())

# 文章详情
def article_detail(request, id):
    
    try:
        # 取出对应文章
        # article = ArticlePost.objects.get(id=id)
        article = get_object_or_404(ArticlePost, id=id)
        # 取出对应评论
        comments = Comment.objects.filter(article=id)
    except Exception as e:
        print(e)
    article.total_view += 1
    #  这个如果使用article.save()是更新所有字段，没有设置新值的字段也需要重新赋予一下原来的值，使用下面更新指定字段
    article.save(update_fields=['total_view'])
    
    delete_comment = False
    if request.user == article.author:
        delete_comment = True
    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 支持目录扩展
        'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    # 需要传递给模版的对象
    context = {'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form, "delete_comment": delete_comment } 

    # 载入模版，并返回context对象 这里不能使用locals() 会把上面没有convert的md变量给拿过去，导致显示不出来目录
    return render(request, 'article/detail.html', context)

def article_create(request):
    # 判断用户请求方式
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提及到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中，id=1的用户为作者
            # 如果你进行删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 保存tags的多对多关系需要用save_m2m方法
            # article_post_form.save_m2m()
            # article_post_form.save()

            # 完成后返回到文章列表
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内存错误，请重新填写。")
    # 如果用户为请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        article_columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'article_columns': article_columns }
        # 返回模块
        return render(request, 'article/create.html', locals())

# 非安全删除文章
def article_delete(request, id):
    # 根据ID获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用删除delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")

# 安全删除文章
def article_safe_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    user = User.objects.get(id=article.author_id)
    # 判断当前修改的用户是否为属主用户
    if request.user == user:    
        if request.method == 'POST':
            article = ArticlePost.objects.get(id=id)
            article.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("仅允许post请求")
    else:
        return HttpResponse("not permission")

# 更新文章
def article_update(request, id):
    """
    更新文章的试图函数
    通过POST方法提交表单，更新title，body字段
    GET方法进入初始表单页面
    id：文章的id
    """

    # 获取需要修改的具体文章对象
    # article =ArticlePost.objects.get(id=id)
    article= get_object_or_404(ArticlePost, id=id)

    # 判断是用户是否为POST方法
    if request.method == 'POST':
        user = User.objects.get(id=article.author_id)
        # 判断当前修改的用户是否为属主用户
        if request.user == user:
            # 将提交的数据赋值到表单中
            article_post_form = ArticlePostForm(instance=article, data=(request.POST))
            # 判断提交的数据是否满足模型要求
            if article_post_form.is_valid():
                # 保存新写入的 title body数据并保存
                # article.title = request.POST['title']
                # article.body = request.POST['body']
                # article.column_id = request.POST['column']
                # article.tags = request.POST['tags']
                # article = article_post_form.save()
                # article.save()
                new_article=article_post_form.save(commit=False)
                # 这个avatar名字和html中的name对应
                if request.FILES:
                    new_article.avatar = request.FILES['avatar']
                    new_article.save()
                new_article.save()

                # 完成后返回修改的文章中。需要传入文章ID
                return redirect("article:article_detail", id=id)
            # 如果数据不合法，返回错误信息
            else:
                return HttpResponse("表单内容有误，请重新填写。")
        else:
            return HttpResponse("没有权限")
    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文, 将article文章对象也传递进去，以便提取更旧的内容
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns}

        # 将响应返回到模版中
        return render(request, 'article/update.html', locals())



