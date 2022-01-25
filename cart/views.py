from django.shortcuts import render

from rest_framework import views, generics, response, status, permissions

from cart.serializer import *
from store.models import PriceTime
from common.permissions import IsConsumer
from common.mixins import ValidateSerializerMixin

class GetCart(ValidateSerializerMixin, generics.GenericAPIView):
    permission_classes = (IsConsumer, )
    serializer_class = CartSerializer

    def get(self, request):
        cart = request.user.consumer.get_cart()
        return response.Response(self.serializer_data(cart))

class AddItem(ValidateSerializerMixin, generics.GenericAPIView):
    permission_classes = (IsConsumer, )
    serializer_class = CartAddItemSerializer

    def post(self, request):
        self.validate(request)
        item_pk = request.data['item']
        vehicle_model_pk = request.data['vehicle_model']

        item = PriceTime.objects.get(pk=item_pk)
        cart = request.user.consumer.get_cart()

        cart.addItem(item, vehicle_model_pk)

        serializer = CartSerializer(cart)
        data = serializer.data

        return response.Response(data, status=status.HTTP_200_OK)

class RemoveItem(ValidateSerializerMixin, generics.GenericAPIView):
    permission_classes = (IsConsumer, )
    serializer_class = CartRemoveItemSerializer

    def post(self, request):
        self.validate(request)
        item_pk = request.data['item']

        item = PriceTime.objects.get(pk=item_pk)
        cart = request.user.consumer.get_cart()

        cart.removeItem(item)

        serializer = CartSerializer(cart)
        data = serializer.data

        return response.Response(data, status=status.HTTP_200_OK)

class ClearCart(ValidateSerializerMixin, generics.GenericAPIView):
    permission_classes = (IsConsumer, )
    serializer_class = ClearCartSerializer

    def post(self, request):
        cart = request.user.consumer.get_cart()
        cart.clear()

        return response.Response(status=status.HTTP_200_OK)
