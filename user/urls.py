"""
URL configuration for market01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from user import views

urlpatterns = {
    # 登录
    path('login/', views.LoginView.as_view()),
    # 注册
    path('register/', views.RegisterView.as_view()),
    # 刷新token
    path('token/refresh/', TokenRefreshView.as_view()),
    # 校验token
    path('token/verify/', TokenVerifyView.as_view()),
    # 获取单个用户信息
    path('<int:pk>/', views.UserView.as_view({'get': 'retrieve'})),
    # # 查看个人信息
    # path('<int:pk>/info/'),
    # 上传用户头像的接口
    path('<int:pk>/avatar/upload/', views.UserView.as_view({'post': 'upload_avatar'})),
    # 添加地址和获取地址列表路由
    path('address/', views.AddressView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    # 修改和删除收货地址
    path('address/<int:pk>/', views.AddressView.as_view({
        'delete': 'destroy',
        'put': 'update',
    })),
    # 设置默认收货地址
    path('address/<int:pk>/default/', views.AddressView.as_view({
        'put': 'set_default_address'
    })),
    # 发送邮件(待修改，若用户有邮箱，则向用户邮箱发送邮件)
    path('email/send/', views.SendEmailView.as_view()),

}
