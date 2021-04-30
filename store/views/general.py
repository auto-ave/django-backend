from rest_framework import generics
from common.permissions import *

from store.models import *
from store.serializers.general import *

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

