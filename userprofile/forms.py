# 引入表单类
from curses.ascii import US
from dataclasses import field
#from charset_normalizer import models
from django import forms
# 引入User模型
from django.contrib.auth.models import User
# 引入Profile模型
from .models import Profile

# 登陆表单， 继承了 form.From 类
# 对数据库进行操作的表单应该继承forms.ModelForm，可以自动生成模型中已有的字段。
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegistryForm(forms.ModelForm):
    # 复写User的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对比两次密码是否一致， def clean_[字段]这种写法Django会自动调用
    def clean_password2(self):
        # self.cleaned_data 属性是用户post的数据清洗之后的字典
        data = self.cleaned_data
        print(data)
        # 从POST中取值用的data.get('password')是一种稳妥的写法，即使用户没有输入密码也不会导致程序错误而跳出。
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
