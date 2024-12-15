from rest_framework import serializers

from .models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    """商品模型序列化器"""

    class Meta:
        model = Goods
        fields = '__all__'
