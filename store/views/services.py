from django.shortcuts import get_object_or_404
from django.db.models import Case, Value, When
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from misc.models import ErrorLogging
from store.models import Store
from common.models import Service, ServiceTag
from store.serializers.services import *
import traceback as tb


class StoreServicesList(generics.ListAPIView):
    serializer_class = PriceTimeListSerializer
    filterset_fields = ['vehicle_type', ]

    def get_queryset(self):
        # slug = self.kwargs['slug']
        # store = get_object_or_404(Store, slug=slug)
        # return store.pricetimes.all().prefetch_related('service')
        # FUTURE: check which query is better
        first_service_tag = self.request.query_params.get('first_service_tag', None)
        
        pricetimes = PriceTime.objects.filter(
                store__slug=self.kwargs['slug'], is_offer=False
            ).prefetch_related('service', 'service__tags', 'store')
        
        if first_service_tag:
            try:
                tag = get_object_or_404(ServiceTag, slug=first_service_tag)
                
                return pricetimes.annotate(
                    is_matching=Case(
                        When(service__tags__in=[tag], then=Value(True)),
                        default=Value(False),
                    ),
                ).order_by('-is_matching')
            except Exception as e:
                ErrorLogging.objects.create(
                    exception=str(e),
                    traceback=tb.format_exc()
                )

        return pricetimes
