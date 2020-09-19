# -*- coding = utf-8 -*-
# @Time : 2020/9/18 20:50
# @Author : jack
# @File : urls.py
# @Software : PyCharm
from django.urls import path
#部署正在应用的名称
app_name = 'comment'

from . import views

urlpatterns = [
    #发表评论处理一级回复
    path('post-comment/<int:article_id>',views.post_comment,name='post_comment'),
    #处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]
