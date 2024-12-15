from django.core.cache import cache
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from cart.models import Cart
from cart.serializers import CartSerializer
from common.cache import goods_list_cache_set
from goods.serializers import GoodsSerializer
from .models import Goods
from .permission import IsAdminUser


class GoodsPagination(PageNumberPagination):
    page_size = 10  # 每页显示10条记录


class AdminGoodsView(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = GoodsPagination

    @method_decorator(goods_list_cache_set(120))
    def list(self, request, *args, **kwargs):
        print('view in')
        return super().list(request, *args, **kwargs)

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


class UserGoodsView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Goods.objects.filter(status=True, remain__gt=0)
    serializer_class = GoodsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GoodsPagination

    @method_decorator(goods_list_cache_set(120))
    def list(self, request, *args, **kwargs):
        print('view in')
        return super().list(request, *args, **kwargs)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            goods = Goods.objects.get(pk=pk)
        except Goods.DoesNotExist:
            return Response({'error': '商品不存在'}, status=status.HTTP_404_NOT_FOUND)
        if goods.remain <= 0:
            return Response({'error': '商品库存不足'}, status=status.HTTP_400_BAD_REQUEST)
        cart, created = Cart.objects.get_or_create(user=user)
        quantity = request.data.get('quantity', 1)  # 默认添加1个商品
        ans = cart.add_goods(goods_id=goods.id, name=goods.name, price=goods.price, quantity=quantity, is_status=goods.status)
        if ans == -1:
            return Response({'error': '商品已下架'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
