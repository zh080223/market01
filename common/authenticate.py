# 自定义用户登录认证模块，实现多字段登录
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import serializers
from user.models import User


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
        except:
            raise serializers.ValidationError({'error': '用户名/邮箱/手机号不存在'})
        else:
            # 验证密码是否正确
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError({'error': '密码错误'})
