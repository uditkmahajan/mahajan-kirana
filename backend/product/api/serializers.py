from product.models import Category, Product, Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer) :
    username = serializers.SerializerMethodField(read_only = True)
    class Meta :
        model = Review
        exclude = ['id']
        extra_kwargs = {
            'user' : {
                'write_only': True
            },
            'product' : {
                'write_only': True
            }
        }
    
    def get_username(self, obj) :
        return obj.user.username

                  
class ProductSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Product
        exclude = ['category', 'is_active', 'dukan']


class CategorySerializer(serializers.ModelSerializer): 
    class Meta :
        model = Category
        exclude = ['id']
        