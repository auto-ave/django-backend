from rest_framework import generics
from django.shortcuts import get_object_or_404

from booking.models import *
from booking.serializers.review import ReviewSerializer


class StoreReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        store = get_object_or_404(Store, slug=slug)
        return store.reviews.all()