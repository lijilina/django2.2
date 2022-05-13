from audioop import add
from inspect import classify_class_attrs
from django.contrib import admin
from .models import drf_Article

class drf_ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'status', 'create_date')
    list_filter = ('status', )
    list_per_page = 10


admin.site.register(drf_Article, drf_ArticleAdmin)
