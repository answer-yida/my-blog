# -*- coding = utf-8 -*-
# @Time : 2020/9/17 22:35
# @Author : jack
# @File : forms.py
# @Software : PyCharm
#引入表单类
from django import forms
#引入user模型
from django.contrib.auth.models import User
from .models import Profile

#登录表单，继承forms，form类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    #复写user密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model =User
        fields = ('username','email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('两次输入密码不一致，请从新输入')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone','avatar','bio')

