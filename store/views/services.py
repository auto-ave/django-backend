import re
from textwrap import indent
from venv import create
from django.shortcuts import get_object_or_404
from django.db.models import Case, Value, When, Max, Count
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from misc.models import ErrorLogging
from store.models import Store
from common.models import Service, ServiceTag
from vehicle.models import *
from store.serializers.services import *
import traceback as tb
import requests, json


class StoreServicesList(generics.ListAPIView):
    serializer_class = PriceTimeListSerializer
    filterset_fields = ['vehicle_type', ]

    def get_queryset(self):
        slug = self.kwargs['slug']
        # store = get_object_or_404(Store, slug=slug)
        # return store.pricetimes.all().prefetch_related('service')
        # FUTURE: check which query is better
        
        
        pricetimes = PriceTime.objects.filter(
                store__slug=slug, is_offer=False
            ).prefetch_related('service', 'service__tags', 'store')
        
                
        first_service_tag = self.request.query_params.get('first_service_tag', None)
        if first_service_tag:
            try:
                tag = get_object_or_404(ServiceTag, slug=first_service_tag)
                
                tag_order_case = Case(
                    When(service__tags__in=[tag.id], then=Value(False)),
                    default=Value(True)
                )
                ordered_pricetimes = pricetimes.order_by(tag_order_case)

                return ordered_pricetimes
                
                # unique_fields = ['id']
                # duplicates = (
                #     ordered_pricetimes.values(*unique_fields)
                #     .annotate(max_id=Max('id'), count_id=Count('id'))
                #     .filter(count_id__gt=1)
                # )
                
                # print(duplicates)
                # print("duplicates count: ", duplicates.count())
                
                unique_ids = ordered_pricetimes.values_list('id', flat=True).distinct()
                print('hopefully ordered ids: ', unique_ids)
                final_pricetimes = PriceTime.objects.filter(id__in=unique_ids)
                print('final ordered ids: ', final_pricetimes.values_list('id', flat=True).distinct())
                return final_pricetimes
        
            except Exception as e:
                ErrorLogging.objects.create(
                    exception=str(e),
                    traceback=tb.format_exc()
                )

        return pricetimes
