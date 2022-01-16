from django.db.models import query
from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny
from cart.serializer import CartSerializer
from common.mixins import ValidateSerializerMixin
from common.permissions import *
from booking.models import Offer
from booking.serializers.offer import *


class  OfferListView(generics.ListAPIView):
    serializer_class = OfferListSerializer
    permission_classes = (IsConsumer,)
    queryset = Offer.objects.filter(is_active=True)

class OfferBannerView(generics.ListAPIView):
    serializer_class = OfferBannerSerializer
    permission_classes = (AllowAny,) 
    queryset = Offer.objects.filter(is_active=True, is_promo=True)

class OfferApplyView(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = OfferApplySerializer
    permission_classes = (IsConsumer,)
    
    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        user = request.user

        cart = user.consumer.get_cart()

        code = data.get('code')
        try:
            offer = Offer.objects.get(code=code)
        except Offer.DoesNotExist:
            return response.Response({
                'error': 'Invalid code'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not offer.is_valid():
            return response.Response({
                'error': 'Offer has Expired'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if cart.items.all().count() == 0:
            return response.Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if offer.max_redeem_count != 0:
            offer_redeems_count = offer.redeems.all().count()
            if offer_redeems_count > offer.max_redeem_count:
                return response.Response({
                    'error': 'Offer has been fully redeemed'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if offer.max_redeem_count_per_cosumer != 0:
            consumer_redeems_count = user.consumer.redeems.all().count()
            if consumer_redeems_count > offer.max_redeem_count_per_cosumer:
                return response.Response({
                    'error': 'You cannot use this offer more than {} times'.format(offer.max_redeem_count_per_cosumer)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        cart.offer = offer
        cart.save()

        return response.Response({
            'success': 'Offer applied successfully',
            'cart': CartSerializer(cart).data
        })

class OfferRemoveView(generics.GenericAPIView):
    serializer_class = OfferRemoveSerializer
    permission_classes = (IsConsumer,)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = user.consumer.get_cart()
        
        cart.offer = None
        cart.save()

        return response.Response({
            'success': 'Offer removed successfully',
            'cart': CartSerializer(cart).data
        })