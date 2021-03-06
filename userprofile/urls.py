# -*- coding = utf-8 -*-
# @Time : 2020/9/18 9:58
# @Author : jack
# @File : urls.py
# @Software : PyCharm
from django.urls import path
from . import views
app_name = 'userprofile'
urlpatterns = [
    #用户登录
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    #用户的删除
    path('delete/<int:id>/',views.user_delete,name='delete'),
    # 用户信息
    path('edit/<int:id>/', views.profile_edit, name='edit'),
]
