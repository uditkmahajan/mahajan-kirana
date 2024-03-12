from dukandar.models import ApniDukan
from product.models import Product
from order.models import Order
from rest_framework import serializers

class ApniDukanSerializer(serializers.ModelSerializer) :
    total_product = serializers.SerializerMethodField(read_only = True)
    # total_order = serializers.SerializerMethodField(read_only = True)
    
    class Meta :
        model = ApniDukan
        fields = '__all__'
    
    def get_total_product(self, obj) :
        return len(Product.objects.filter(dukan = obj.id))
    
    # def get_total_order(self, obj) :
    #     return Order.objects.filter(dukan_id = obj)     