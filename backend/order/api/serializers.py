from order.models import Order, OrderItem
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer) :
    product_name = serializers.SerializerMethodField(read_only = True)
    product_id = serializers.SerializerMethodField(read_only = True)
    product_price = serializers.SerializerMethodField(read_only = True)
    offer = serializers.SerializerMethodField(read_only = True)
    image = serializers.SerializerMethodField(read_only = True)
    class Meta :
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'product' : {
                'write_only' : True
            }
        }
        
    def get_product_name(self, obj) :
        return obj.product.name
    
    def get_product_id(self, obj) :
        return obj.product.id
    
    def get_product_price(self, obj) :
        return obj.product.price
    
    def get_offer(slf, obj) :
        return obj.product.offer
    
    def get_image(self, obj) :
        try : 
            return obj.product.image.url
        except Exception as e :
            return obj.product.url
   
    
class OrderSerializer(serializers.ModelSerializer) :
    username = serializers.SerializerMethodField(read_only = True)
    
    class Meta :
        model = Order
        exclude = ['user']
    
    def validate_order_house_no(self, house_no)  :
        try :  
            if int(house_no) > 0 :
                return house_no
            else :
                raise serializers.ValidationError('House number should be valid!')
        except Exception as e :
            raise serializers.ValidationError('Please enter only numeric value!')
    
    def validate_order_pin(self, pin) :
        try :
            if len(str(pin)) == 6 and int(pin) :
                 return pin
            else :
                raise serializers.ValidationError('Pin must contain 6 characters!')
        except Exception as e :
            raise serializers.ValidationError('Please enter only numerice value!')
    
    
    def validate_order_phone_number(self, phone_number) :
        try :
            if len(str(phone_number)) == 10 and int(phone_number):
                return phone_number 
            raise serializers.ValidationError('Phone Number must contain 10 digits!')
        except Exception as e :
            raise serializers.ValidationError('Phone Number must contain only numbers!')
        
    def get_username(self, obj) :
        return obj.user.username
    
