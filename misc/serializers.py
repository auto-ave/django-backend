from rest_framework import serializers
from misc.models import *
class ImageSerializer(serializers.Serializer):
    image = serializers.FileField(read_only=True)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('message', 'order_id')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')