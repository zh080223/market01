from django.db import models
from rest_framework import status
from rest_framework.response import Response

from user.models import User


# Create your models here.
# 购物车模型
class Cart(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=User, on_delete=models.CASCADE)
    goods = models.JSONField(verbose_name='商品', default=None)
    '''
    Json数据结构
    {
        'nums': 3
        'goods': [
            {
                'goods_id': 1,
                'name': 'cola',
                'quantity': 1,
                'total_price': 9.9
            }
        ]
    }
    Json数据结构
    '''

    def add_goods(self, goods_id, name, price, quantity, is_status):
        # 检查商品是否已在购物车中
        found = False
        if not is_status:
            return -1
        for item in self.goods.get('items', []):
            if item['goods_id'] == goods_id:
                item['quantity'] += quantity
                item['total_price'] = item['quantity'] * price  # 更新总价格
                found = True
                break  # 找到商品后不需要继续循环
        if not found:
            # 添加新商品到购物车
            self.goods['nums'] += 1
            self.goods['items'].append({
                'goods_id': goods_id,
                'name': name,
                'quantity': quantity,
                'total_price': price * quantity,
            })
        self.save()  # 保存购物车的最新状态

    def remove_goods(self, goods_id):
        # 移除购物车中的商品
        self.goods['items'] = [item for item in self.goods.get('items', []) if item.get('goods_id') != goods_id]
        self.save()

    def update_goods_quantity(self, goods_id, quantity):
        # 更新购物车中的商品数量
        for item in self.goods.get('items', []):
            if item.get('goods_id') == goods_id:
                old_quantity = item['quantity']
                item['quantity'] = quantity
                item['total_price'] = item.get('total_price') / old_quantity * quantity
                break
        self.save()
