from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from goods.serializers import GoodsSerializer
from .models import Goods
from .permission import IsAdminUser
from cart.models import Cart
from cart.serializers import CartSerializer


# Create your views here.

######
# 1.商品加入购物车接口
######

# admin可以增删改查

class GoodsPagination(PageNumberPagination):
    page_size = 10  # 每页显示10条记录


class AdminGoodsView(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = GoodsPagination

    def set_status(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status:
            obj.status = not obj.status
            obj.save()
            return Response({'message': '下架成功'}, status=status.HTTP_200_OK)
        else:
            obj.status = not obj.status
            obj.save()
            return Response({'message': '上架成功'}, status=status.HTTP_200_OK)


# 普通用户只能查询
class UserGoodsView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Goods.objects.filter(status=True, remain__gt=0)
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GoodsPagination


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    # 向购物车新增商品
    def post(self, request, pk):
        # 获取当前登录的用户
        user = request.user
        # 根据商品ID获取商品对象
        try:
            goods = Goods.objects.get(pk=pk)
        except Goods.DoesNotExist:
            return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)
        # 检查商品是否有足够的库存
        if goods.remain <= 0:
            return Response({'error': '商品库存不足'}, status=status.HTTP_400_BAD_REQUEST)
        # 获取或创建用户的购物车
        cart, created = Cart.objects.get_or_create(user=user)
        # 从请求中获取商品数量
        quantity = request.data.get('quantity', 1)  # 默认添加1个商品
        # 调用购物车模型的add_goods方法添加商品
        cart.add_goods(goods_id=goods.id, name=goods.name, price=goods.price, quantity=quantity)
        # 序列化购物车对象并返回响应
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
