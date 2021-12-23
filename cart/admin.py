from django.contrib import admin

from cart.models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ( 'consumer', 'store', 'vehicle_model', 'subtotal', 'total' )
    list_filter = ( 'store', )
    search_fields = ( 'consumer__user__first_name', 'consumer__user__last_name', 'consumer__user__email' , 'consumer__user__phone', 'store__name' )