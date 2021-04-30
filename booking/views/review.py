from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from common.permissions import *

from booking.models import *
from booking.serializers.review import *

class ReviewListCreate(generics.ListCreateAPIView):
    permission_classes = ( IsConsumer, )
    filter_backends = ( DjangoFilterBackend, )
    filter_fields = ( 'store', )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        else:
            return ReviewSerializer
    
    def get_queryset(self):
        user = self.request.user
        print(Review.objects.all())
        return Review.objects.filter(consumer=user.consumer)
    
    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(consumer=user.consumer)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( IsConsumer,  )