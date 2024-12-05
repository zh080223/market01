from rest_framework import serializers

from user.models import User, Address


class UserSerializer(serializers.ModelSerializer):
    """用户模型序列化器"""

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'mobile',
            'avatar',
            'last_name',
        ]


class AddressSerializer(serializers.ModelSerializer):
    """收货地址模型序列化器"""

    class Meta:
        model = Address
        fields = '__all__'
