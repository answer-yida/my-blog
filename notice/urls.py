# -*- coding = utf-8 -*-
# @Time : 2020/9/19 16:30
# @Author : jack
# @File : urls.py
# @Software : PyCharm
from django.urls import path
from . import views
app_name = 'notice'
urlpatterns = [
    # 通知列表
    path('list/', views.CommentNoticeListView.as_view(), name='list'),
    # 更新通知状态
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'),
]