from django.db.models import query
from rest_framework import generics, response
from common.mixins import ValidateSerializerMixin
from common.permissions import *
from booking.models import Offer
from booking.serializers.offer import *


class OfferListView(generics.ListAPIView):
    serializer_class = OfferSerializer
    permission_classes = (IsConsumer,)
    queryset = Offer.objects.active_offers()

class OfferApplyView(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = OfferApplySerializer
    permission_classes = (IsConsumer,)
    
    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        user = request.user
        
        code = data.get('code')
        cart = user.consumer.get_cart()
        
        
        return response.Response({})