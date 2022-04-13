from django.contrib import admin

# 导入新建ArticlePost
from .models import ArticlePost, ArticleColumn

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)
# 注册ArticleColumn到admin中
admin.site.register(ArticleColumn)

