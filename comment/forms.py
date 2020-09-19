# -*- coding = utf-8 -*-
# @Time : 2020/9/18 21:04
# @Author : jack
# @File : forms.py
# @Software : PyCharm
from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
