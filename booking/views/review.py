from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import *
from django.shortcuts import get_object_or_404
from booking.models import *
from booking.serializers.review import *

class ReviewListCreate(generics.CreateAPIView):
    permission_classes = ( IsConsumer, )
    serializer_class = ReviewCreateSerializer
    lookup_field = 'booking_id'

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(consumer=user.consumer)

class ReviewRetrieve(generics.RetrieveAPIView):
    permission_classes = ( IsConsumer, )
    serializer_class = ReviewSerializer

    def get_object(self):
        return get_object_or_404(Review, booking_id=self.kwargs['booking_id'])