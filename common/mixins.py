from rest_framework import serializers

class ValidateSerializerMixin:
    def validate(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.data
    
    def serializer_data(self, data):
        serializer = self.get_serializer(data)
        return serializer.data