from unicodedata import name
from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registry/', views.user_registry, name='registry'),
    path('delete/<int:uid>/', views.user_delete, name='delete'),
    path('edit/<int:id>/', views.profile_edit, name='edit')
]