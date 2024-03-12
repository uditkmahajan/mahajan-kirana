from django.contrib import admin
from .models import ApniDukan

# Register your models here.
class ApniDukanAdmin(admin.ModelAdmin) :
    model = ApniDukan
    list_display = ('id', 'name', 'owner', 'area', 'phone_number', 'slug', 'is_active')
    search_fields = ('name', 'owner', 'area')
    list_filter = ('area', 'is_active')
    fieldsets = (
        ('None', {'fields' :('name', 'owner', 'area')}),
        ('Detail', {'fields' :('phone_number', 'whatsapp_number', 'about', 'delivery_detail', 'is_active')}),
        ('Images', {'fields' :('owner_image', 'banner_image')}),
    )

admin.site.register(ApniDukan, ApniDukanAdmin)