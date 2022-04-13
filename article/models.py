from ctypes import resize
from distutils.command.upload import upload
from re import I
from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
# 导入Django内建User模型
from django.contrib.auth.models import User
from django.forms import CharField
# timezone 用于处理时间相关事物
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class ArticleColumn(models.Model):
    """
    栏目的models
    """
    title  = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title


# 博客文章数据类型
class ArticlePost(models.Model):
    # 文章作者 外健关联Django的User表，参数 on_delete 用于指定数据删除的方式 级联删除
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题 models.CharField 为字符串字段，用于保存较短的字符串 如标题
    title = models.CharField(max_length=100)

    # 文章正文 保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间 参数default=timezone.now 指定在其创建时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间 参数 auto_now = True 指定每次更新时自动写入当前
    updated = models.DateTimeField(auto_now=True)

    # 文章浏览量
    total_view = models.PositiveIntegerField(default=0)

    # 文章栏目的的“一对多” 外键
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article' )

    # 文章标签 已废除 使用独立表
    tags = models.CharField(max_length=100, default='speical')

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank = True)

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            # resize_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resize_image = image.resize((400, 300), Image.ANTIALIAS)
            resize_image.save(self.avatar.path)
        return article
    # 内部类 class Meta 用于给model定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒叙排序
        ordering = ('-created',)

    # 函数 __str__(self):
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        # 通过reverse()方法返回文章详情页面的url，实现了路由重定向。
        return reverse("article:article_detail", kwargs={"id": self.id})

# class Article_tag(models.Model):
#     tag = models.CharField(max_length=50, verbose_name="文章tag")
#     article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, verbose_name="文章id")
    
#     class Meta:
#         db_table = 'Article_tag'
#     def __str__(self):
#         return self.article
    

# 测试 http://djangobook.py3k.cn/2.0/chapter10/

# class Publisher(models.Model):
#     name = models.CharField(max_length=30)
#     address = models.CharField(max_length=50)
#     city = models.CharField(max_length=60)
#     state_province = models.CharField(max_length=30)
#     country = models.CharField(max_length=50)
#     website = models.URLField()

#     def __unicode__(self):
#         return self.name

# class Author(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=40)
#     email = models.EmailField()

#     def __unicode__(self):
#         return u'%s %s' % (self.first_name, self.last_name)

# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     authors = models.ManyToManyField(Author)
#     publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
#     publication_date = models.DateField()

#     def __unicode__(self):
#         return self.title

