from django.contrib import admin
from django.core.exceptions import ValidationError

from cart.models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ( 'consumer', 'store', 'vehicle_model', 'subtotal', 'total' )
    list_filter = ( 'store', )
    search_fields = ( 'consumer__user__first_name', 'consumer__user__last_name', 'consumer__user__email' , 'consumer__user__phone', 'store__name' )
    readonly_fields = ('discount', 'total', 'subtotal', 'store', 'offer', 'vehicle_model', 'items' )
    
    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().prefetch_related('consumer', 'consumer__user', 'store', 'vehicle_model', 'vehicle_model__brand')
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_object(self, request, object_id, from_field=None):
        queryset = self.get_queryset(request)
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)
        try:
            object_id = field.to_python(object_id)
            return queryset.get(**{field.name: object_id})
        except (model.DoesNotExist, ValidationError, ValueError):
            return None