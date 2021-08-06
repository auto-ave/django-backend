from rest_framework import serializers

from store.models import Bay

class InitiateTransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    bay = serializers.PrimaryKeyRelatedField(queryset=Bay.objects.all())
    slot_start = serializers.TimeField()
    slot_end = serializers.TimeField()
    