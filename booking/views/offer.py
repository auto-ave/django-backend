from django.db.models import query
from rest_framework import generics, response
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
    permission_classes = (IsConsumer,)
    queryset = Offer.objects.filter(is_active=True, is_promo=True)

class OfferApplyView(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = OfferApplySerializer
    permission_classes = (IsConsumer,)
    
    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        user = request.user
        
        code = data.get('code')
        cart = user.consumer.get_cart()

        offer = Offer.objects.get(code=code)
        if not offer.is_valid():
            return response.Response({
                'error': 'Offer has Expired'
            })

        cart.apply_offer(offer)
        
        
        return response.Response({})