from django.contrib import admin
from .models import Category, Product, Review

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'name', 'slug', 'total_products')
    search_fields = ('name', 'slug', 'total_products')
    ordering = ('slug',)
    list_filter = ('total_products',)
    fieldsets = (
        ('Detail', {'fields': ('name', 'slug', 'total_products', 'image')}),
    )
    
class ProductAdmin(admin.ModelAdmin) : 
    model = Product
    list_display = ('id', 'slug', 'category', 'avg_rating', 'total_reviews','mrp', 'price', 'is_active') 
    search_fields = ('slug', 'category', 'avg_rating', 'total_reviews', 'price', 'is_active') 
    ordering = ('slug',)
    list_filter = ('price', 'total_reviews', 'is_active', 'avg_rating', 'category')
    fieldsets = (
        (None, {
            "fields": (
                'name', 'slug', 'category', 'image' , 'url', 'dukan'
            ),
        }),
        ('Detail', {
             "fields": (
                 'avg_rating', 'total_reviews','mrp', 'price', 'discount', 'is_active', 'description', 'offer',
             )   
        })
    )
    
class ReviewAdmin(admin.ModelAdmin) :
    model = Review
    list_display = ('id', 'user', 'rating', 'product')
    search_fields = ('user', 'rating', 'product')
    ordering = ('rating',)
    list_filter = ('user', 'rating', 'product')
    fieldsets = (
        ('None', {'fields': ('user', 'rating', 'product', 'comment')}),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
