# -*- coding = utf-8 -*-
# @Time : 2020/9/17 17:50
# @Author : jack
# @File : urls.py
# @Software : PyCharm
from django.urls import path
#部署正在应用的名称
app_name = 'article'

from . import views
urlpatterns = [
    #path函数将url映射到视图
    path('article-list/',views.article_list,name='article_list'),
    path('article-detail/<int:id>/',views.article_detail,name='article_detail'),
    path('article-create/',views.article_create,name='article_create'),
    path('article-delete/<int:id>/',views.article_delete,name='article_delete'),
    # 安全删除文章
    path(
        'article-safe-delete/<int:id>',
        views.article_safe_delete,
        name='article_safe_delete'
    ),
    #更新文章
    path('article-update/<int:id>/', views.article_update, name='article_update'),

    # 点赞 +1
    path(
        'increase-likes/<int:id>/',
        views.IncreaseLikesView.as_view(),
        name='increase_likes'
    ),
]