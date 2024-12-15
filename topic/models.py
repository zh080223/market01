from django.db import models

from user.models import User


# Create your models here.
class Topic(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    into = models.CharField(verbose_name='简介', max_length=100)
    content = models.TextField(verbose_name='内容')
    # 推荐类 & 日常类
    category = models.CharField(verbose_name='分类', max_length=20)
    # 公开的 & 私密的
    limit = models.CharField(verbose_name='权限', max_length=20)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    author = models.ForeignKey(verbose_name='作者', to=User, on_delete=models.CASCADE)
