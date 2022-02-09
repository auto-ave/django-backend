from rest_framework import serializers
from booking.models import Offer
from store.models import PriceTime

class OfferListSerializer(serializers.ModelSerializer):
    saving = serializers.SerializerMethodField()
    
    class Meta:
        model = Offer
        exclude = ('discount_percentage', 'max_discount', 'max_redeem_count', 'max_redeem_count_per_cosumer', 'valid_from', 'valid_to')

    
    def get_saving(self, obj):
        offer = obj
        user = self.context['request'].user
        cart = user.consumer.cart
        
        if cart.items.all().count() == 0:
            return 'Cart is empty'
        
        if offer.max_redeem_count != 0:
            offer_redeems_count = offer.redeems.all().count()
            if offer_redeems_count > offer.max_redeem_count:
                return 'Offer has been fully redeemed'
        
        if offer.max_redeem_count_per_cosumer != 0:
            consumer_redeems_count = user.consumer.redeems.all().count()
            if consumer_redeems_count > offer.max_redeem_count_per_cosumer:
                return 'You cannot use this offer more than {} times'.format(offer.max_redeem_count_per_cosumer)
        
        saving_amount = offer.get_discount_amount_from_sub_total(cart.subtotal)
        
        services_to_add = offer.services_to_add.all()
        if services_to_add.count():
            saving_amount = 0
            for service in services_to_add:
                price_time = PriceTime.objects.get(store=cart.store, service=service, vehicle_type=cart.vehicle_model.vehicle_type)
                saving_amount += ( price_time.mrp or price_time.price )

        return 'You will save Rs.{} on this order'.format(saving_amount)

class OfferBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('code', 'banner')

class OfferApplySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=21)

class OfferRemoveSerializer(serializers.Serializer):
    pass