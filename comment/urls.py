from unicodedata import name
from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>', views.post_comment, name='post_comment'),
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
    path('delete-comment/<int:comment_id>', views.delete_comment, name="delete_comment"),
]