from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.urls import path, include

urlpatterns = [
    # re_path(r'^articles/$', article_list),
    # re_path(r'articles/(?P<pk>[0-9]+)$', article_detail),
    re_path(r'^articles/$', ArticleList.as_view()),
    re_path(r'^articles/(?P<pk>[0-9]+)$', ArticleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)