from django.db.models import query
from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny
from cart.serializer import CartSerializer
from common.mixins import ValidateSerializerMixin
from common.permissions import *
from booking.models import Offer
from booking.serializers.offer import *
from django.db.models import Q

from store.models import PriceTime


class OfferListView(generics.ListAPIView):
    serializer_class = OfferListSerializer
    permission_classes = (IsConsumer,)
    queryset = Offer.objects.filter(is_active=True)
    
    def get_queryset(self):
        cart = self.request.user.consumer.cart
        queryset = self.queryset.filter(
            Q(min_booking_amount__lte=cart.subtotal, max_booking_amount__gt=cart.subtotal)
            |
            Q( max_booking_amount=0 )
        )
        return queryset

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
        cart_items = cart.items.all()

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
        
        if cart_items.count() == 0:
            return response.Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if offer.linked_store and (offer.linked_store != cart.store):
            return response.Response({
                'error': 'Offer is not valid for this store'
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
        
        if offer.max_booking_amount > 0:
            if cart.subtotal >= offer.max_booking_amount:
                return response.Response({
                    'error': 'Offer cannot be applied on bookings greater than Rs.{}'.format(offer.max_booking_amount)
                }, status=status.HTTP_400_BAD_REQUEST)

            if cart.subtotal < offer.min_booking_amount:
                return response.Response({
                    'error': 'Offer cannot be applied on bookings less than Rs.{}'.format(offer.min_booking_amount)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        applicable_services = offer.applicable_services.all()
        flag = False
        if len(applicable_services):
            for item in cart_items:
                if item.service in applicable_services:
                    flag = True
                    break
            if not flag:
                return response.Response({
                    'error': 'Offer cannot be applied for selected services'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        
        cart.offer = offer
        cart.save()

        return response.Response({
            'success': 'Offer applied successfully',
            'cart': CartSerializer(cart, context={
                'request': request
            }).data
        })

class OfferRemoveView(generics.GenericAPIView):
    serializer_class = OfferRemoveSerializer
    permission_classes = (IsConsumer,)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = user.consumer.get_cart()
        offer = cart.offer
        
        if offer:
            offer_services = offer.services_to_add.all()
            
            if offer_services.count():
                for service in offer_services:
                    price_time = PriceTime.objects.get(service=service, store=cart.store, vehicle_type=cart.vehicle_model.vehicle_type)
                    cart.items.remove(price_time)
        
        cart.offer = None
        cart.save()

        return response.Response({
            'success': 'Offer removed successfully',
            'cart': CartSerializer(cart, context={
                'request': request
            }).data
        })