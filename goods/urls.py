from django.urls import path

from .views import AdminGoodsView, UserGoodsView, AddToCartView

'''
1.{{host}}/api/goods/：管理员添加商品
    [post]
    [get]
2.{{host}}/api/goods/?page=1：管理员查询商品并进行分页
3.{{host}}/api/goods/4/：管理员删除商品
4.{{host}}/api/goods/status/3/：管理员上/下架商品
5.{{host}}/api/goods/user/?page=1：普通用户查询商品并分页
'''

urlpatterns = [
    # 以Admin身份登录，可以进行增删改查
    path('', AdminGoodsView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('<int:pk>/', AdminGoodsView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    # 以用户身份登录，只能实现查
    path('user/', UserGoodsView.as_view({
        'get': 'list',
    })),
    path('user/<int:pk>/', UserGoodsView.as_view({
        'get': 'retrieve',
    })),
    # 管理员上下架接口
    path('status/<int:pk>/', AdminGoodsView.as_view({
        'put': 'set_status',
    })),
    path('<int:pk>/add/', AddToCartView.as_view()),
]
