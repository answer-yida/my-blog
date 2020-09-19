from django.contrib import admin
from .models import ArticlePost
from .models import ArticleColumn
admin.site.register(ArticlePost)
#注册文章栏目
admin.site.register(ArticleColumn)