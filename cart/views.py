from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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
