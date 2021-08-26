from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from store.models import Store
from store.serializers.services import *

class StoreServicesList(generics.ListAPIView):
    serializer_class = PriceTimeListSerializer
    filterset_fields = ['vehicle_type',]

    def get_queryset(self):
        slug = self.kwargs['slug']
        store = get_object_or_404(Store, slug=slug)
        return store.pricetimes.all()