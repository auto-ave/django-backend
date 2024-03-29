from common.serializers import ServiceTagSerializer, StoreServiceListTagSerializer
from vehicle.models import VehicleType
from rest_framework import serializers
from store.models import PriceTime, Service,Store

class PriceTimeListSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    time_interval = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_service(self, obj):
        return obj.service_name
    
    def get_time_interval(self, obj):
        return obj.time_interval_string
    
    def get_offer(self, obj):
        offers = obj.store.offers.filter(applicable_services__in=[obj.service])
        first_offer = offers.first()

        if first_offer:
            first_service = first_offer.services_to_add.first()
            first_pricetime = PriceTime.objects.get(service=first_service, store=obj.store, vehicle_type=obj.vehicle_type)
            return {
                'text': 'Get FREE {} worth ₹{} with this service'.format(first_service.name, int(first_pricetime.mrp - first_pricetime.price)),
                'code': first_offer.code,
            }
        return None

    def get_tags(self, obj):
        service = obj.service
        tags = service.tags.all()
        return StoreServiceListTagSerializer(tags, many=True).data

    class Meta:
        model = PriceTime
        fields = "__all__"

class PriceTimeSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    time_interval = serializers.SerializerMethodField()
    class Meta:
        model = PriceTime
        fields = "__all__"
    
    def get_service(self, obj):
        return obj.service_name

    def get_time_interval(self, obj):
        return obj.time_interval_string

class StoreListPriceTimeSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    class Meta:
        model = PriceTime
        fields = ('service', 'price')
    
    def get_service(self, obj):
        return obj.service_name

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ('tags', )

class CreatePriceTimeSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())
    # service = serializers.SerializerMethodField()
    # store = serializers.SerializerMethodField()
    # vehicle = serializers.SerializerMethodField()
    class Meta:
        model = PriceTime
        fields = "__all__"
    
    # def get_service(self, obj):
    #     return Service.objects.get(id=obj.service) 
    # def get_store(self, obj):
    #     return Store.objects.get(id=obj.store)
    # def get_vehicle(self, obj):
    #     return VehicleType.objects.get(id=obj.vehicle_type)  
                 
# class StoreServiceListSerializer(serializers.Serializer):
#     service = ServiceSerializer()
#     min_price = serializers.SerializerMethodField()
#     max_price = serializers.SerializerMethodField()
#     min_slot_length = serializers.SerializerMethodField()
#     max_slot_length = serializers.SerializerMethodField()
    
    
#     def get_min_price(self, obj):
#         return self.context['min_price']
#     def get_max_price(self, obj):
#         return self.context['max_price']
#     def get_min_slot_length(self, obj):
#         return self.context['min_slot_length']
#     def get_max_slot_length(self, obj):
#         return self.context['max_slot_length']                    