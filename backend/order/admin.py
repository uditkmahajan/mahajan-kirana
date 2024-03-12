from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'user', 'is_completed', 'is_deliverd', 'total_price','created_at', 'deliverd_at', 'is_paid')
    list_filter = ('user', 'is_completed', 'is_deliverd', 'deliverd_at', 'is_paid')
    search_fields = ('user', 'is_completed', 'is_deliverd', 'total_price','deliverd_at', 'is_paid') 
    ordering = ('id',)
    fieldsets = (
        (None, {
            "fields": ('user', ),
        }),
        ('Detail', {
             "fields": ('is_completed', 'is_deliverd', 'total_price','deliverd_at', 'is_paid', 'additional', 'order_list')   
        }),
        ( 'Address', {
            'fields' : ('order_username', 'order_house_no', 'order_address', 'order_city', 'order_phone_number', 'order_pin')
        }
            
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'is_completed', 'is_deliverd', 'total_price','created_at' 'deliverd_at', 'is_paid', 'order_username', 'order_house_no', 'order_address', 'order_city', 'order_phone_number', 'order_pin'),
        }),
    )
    
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('product', 'order', 'quantity', 'price')
    list_filter = ('order',)
    search_fields = ('order__id', 'price') 
    ordering = ('order',)
    fieldsets = (
        (None, {
            "fields": ('product', ),
        }),
        ('Detail', {
             "fields": ('order', 'quantity', 'price', 'item_offer')   
        }),
    )
    
    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)