from rest_framework import generics
from common.permissions import *

from store.models import *
from store.serializers.general import *
import haversine as hs
from haversine import Unit
from django.shortcuts import get_object_or_404
class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( ReadOnly | ( IsPartner & IsStoreOwner ) , )

    def get_queryset(self):
        # user = self.request.user
        # params = self.request.query_params

        # partner_query =  params.get('partner')

        # if partner_query:
        #     partners = Partner.objects.filter(pk=partner_query)
        #     if not partners:
        #         return []
        #     return Store.objects.filter(owner=partner)
        
        return Store.objects.all()

    def get_serializer_class(self):
        return StoreSerializer

class StoreList(generics.ListAPIView):
    permission_classes = (ReadOnly | (IsConsumer),)

    def get_serializer_class(self):
        return StoreListSerializer

    def get_queryset(self):
        loc1=(23.3045, 77.4219)
        vehicle_type = get_object_or_404(VehicleType, vehicle_model = "2_four")
        queryset = []
        stores =Store.objects.all()
        for store in stores:
            loc2 = (store.latitude, store.longitude)
            if hs.haversine(loc1, loc2, Unit.METERS) <= 100000 and vehicle_type.store_set.filter(pk = store.pk).exists():
                    queryset.append(store)
        return queryset