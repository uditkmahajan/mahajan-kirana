from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone_number', 'city', 'default_dukan')
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'first_name', 'last_name', 'city', 'area', 'house_no', 'default_dukan')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

admin.site.register(User, CustomUserAdmin)
