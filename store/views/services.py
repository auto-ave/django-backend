from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from store.models import Store
from store.serializers.services import *

class StoreServicesList(generics.ListAPIView):
    serializer_class = PriceTimeListSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vehicle_type', 'vehicle_type__model']

    def get_queryset(self):
        print(self.request.data)

        slug = self.kwargs['slug']
        store = get_object_or_404(Store, slug=slug)

        service = None

        return store.pricetimes.all()