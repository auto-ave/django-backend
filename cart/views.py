from django.shortcuts import render

from rest_framework import views, generics, response, status, permissions

from cart.serializer import *
from store.models import PriceTime

from common.mixins import ValidateSerializerMixin

class GetCart(ValidateSerializerMixin, generics.GenericAPIView):
    serializer_class = CartSerializer

    def get(self, request):
        cart = request.user.consumer.getCart()
        return response.Response(self.serializer_data(cart))

class AddItem(ValidateSerializerMixin, generics.GenericAPIView):
    serializer_class = ItemSerializer

    def post(self, request):
        self.validate(request)

        item = PriceTime.objects.get(pk=request.data['item'])
        cart = request.user.consumer.getCart()

        cart.addItem(item)

        serializer = CartSerializer(cart)
        data = serializer.data

        return response.Response(data, status=status.HTTP_200_OK)

class RemoveItem(ValidateSerializerMixin, generics.GenericAPIView):
    serializer_class = ItemSerializer

    def post(self, request):
        self.validate(request)

        item = PriceTime.objects.get(pk=request.data['item'])
        cart = request.user.consumer.getCart()

        cart.removeItem(item)

        serializer = CartSerializer(cart)
        data = serializer.data

        return response.Response(data, status=status.HTTP_200_OK)

class ClearCart(ValidateSerializerMixin, generics.GenericAPIView):

    def post(self, request):
        cart = request.user.consumer.getCart()
        cart.clear()

        return response.Response(status=status.HTTP_200_OK)
