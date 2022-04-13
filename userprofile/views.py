from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
#from flask import session
from markupsafe import re
#from psutil import users
from .forms import UserLoginForm, UserRegistryForm
from django.contrib.auth.models import User
# 引入验证登陆的装饰器
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法的数据
            data = user_login_form.cleaned_data
            # 检验账号，密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在session 中，即实现了登陆动作
                login(request, user)
                # 获取用户的cookie中存的session ID
                print(request.session.session_key)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入有误，请重新输入～")
        else:
            return HttpResponse("账号密码输入不合法")
    elif request.method == "GET":
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', locals())
    else:
        return HttpResponse("请使用GET或POST请求数据")

def user_logout(request):
    logout(request)
    return redirect("article:article_list")

# 用户注册
def user_registry(request):
    if request.method == 'POST':
        user_registry_form = UserRegistryForm(data=request.POST)
        if user_registry_form.is_valid():
            new_user = user_registry_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_registry_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登陆并返回博客列表页面
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表输入有误，请重新输入～")
    elif request.method == 'GET':
        user_registry_form = UserRegistryForm()
        context = {'user_registry_form': user_registry_form}
        return render(request, 'userprofile/registry.html', locals())
    else:
        return HttpResponse("请使用POST or GET 请求数据")


# 用户删除
@login_required(login_url='/userprofile/login')
def user_delete(request, uid):
    if request.method == 'POST':
        user = User.objects.get(id = uid)
        # 验证码要删除的用户是否为当前登陆用户
        print(request.user)
        if user == request.user:
            #退出登陆，，删除用户并返回博客列表
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除权限")
    else:
        return HttpResponse("请使用post方法")

# 编辑用户信息
@login_required(login_url='/userprofile/login')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    #user_id 是 OneToOneField 自动生成的字段
    # profile = Profile.objects.get(user_id=id)
    # 判断用户是否在表中，如果不在就新插入到表中
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        # 目前请求中只能有用户的user_id，会新插入到userprofile_profile表 且只有user_id 有值
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 判断当前用户和操作用户是否一致，是不是本人
        if request.user != user:
            return HttpResponse('你没有权限修改当前用户')
        
        # 上传的文件保存在 request.FILES中，通过参数传递给form
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据, 写入数据库
            profile_form_cd = profile_form.cleaned_data
            print(profile_form_cd)
            profile.phone = profile_form_cd['phone']
            profile.bio = profile_form_cd['bio']
            
            # 如果文件存在则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_form_cd['avatar']
            
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误！！！")
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'user': user}
        return render(request,'userprofile/edit.html', locals())
    else:
        return HttpResponse("请使用 GET 或 POST请求数据")



            





