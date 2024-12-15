from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from .long_id import generate_order_id
from .models import Cart
from .serializers import CartSerializer


class CartView(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def remove_item(self, request, goods_id):
        cart = Cart.objects.get(user=request.user)
        cart.remove_goods(goods_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update_quantity(self, request, goods_id):
        cart = Cart.objects.get(user=request.user)
        quantity = request.data['quantity']
        cart.update_goods_quantity(goods_id, quantity)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(ModelViewSet):
    # 从购物车生成订单
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def generate_order(self, request):
        cart = Cart.objects.get(user=request.user)
        long_id = generate_order_id()
        user = request.user
        order_status = 1
        amount = 0
        for item in cart.goods.get('items', []):
            amount += item['total_price']
        Order.objects.create(user=user, long_id=long_id, status=order_status, amount=amount)
        return Response({'msg': '订单创建成功'}, status=status.HTTP_201_CREATED)
