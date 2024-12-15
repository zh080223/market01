from django.urls import path

from .views import CartView, OrderView

'''
1.{{host}}/api/cart/：查询当前购物车信息
2.{{host}}/api/cart/2/remove/：删除购物车中某一个商品
3.{{host}}/api/cart/1/update/：更新购物车中某一个商品的数量
'''


urlpatterns = [
    path('', CartView.as_view({
        'get': 'list',
    })),
    path('<int:goods_id>/remove/', CartView.as_view({
        'delete': 'remove_item',
    })),
    path('<int:goods_id>/update/', CartView.as_view({
        'post': 'update_quantity',
    })),
    path('order/', OrderView.as_view({
        'post': 'generate_order',
    }))
]
