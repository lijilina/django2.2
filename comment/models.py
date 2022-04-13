from django.db import models
#倒入Django user表
from django.contrib.auth.models import User
#倒入文章表
from article.models import ArticlePost

#倒入评论 数据类型
#pip install django-ckeditor
from ckeditor.fields import RichTextField

# 倒入多级评论模块
# pip install django-mptt
from mptt.models import MPTTModel, TreeForeignKey


# class Comment(models.Model):
class Comment(MPTTModel):
    # 与文章表外键关联，如果文章表记录删除comment表也删除关联的记录
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    # 与用户表外键关联
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # 评论内容
    # body = models.TextField()
    body = RichTextField()
    # 评论时间 自动添加时间
    created = models.DateTimeField(auto_now_add=True)

    # 新增 mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增, 记录二级评论回复给谁， str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )


    # class Meta:
    class MPTTMeta:
        # 以created自动排序
        ordering  = ('created',)
    def __str__(self):
        # 调试返回body的前20字符串
        return self.body[:20]


# class test_Publication(models.Model):
#     title = models.CharField(max_length=30)

#     class Meta:
#         ordering = ['title']
#         db_table = 'test_Publication'
    
#     def __str__(self) -> str:
#         return  self.title

# class test_Article(models.Model):
#     headline = models.CharField(max_length=100)
#     publications = models.ManyToManyField(test_Publication)

#     class Meta:
#         ordering = ['headline']
#         db_table = "test_Article"

#     def __str__(self) -> str:
#         return self.headline