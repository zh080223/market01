from rest_framework import serializers

from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'goods',
        ]

    def create(self, validated_data):
        cart = Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        goods_data = validated_data.pop('goods', None)
        if goods_data:
            instance.goods = goods_data
        instance.save()
        return instance
