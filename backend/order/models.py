from django.db import models
from User.models import User
from django.utils.text import slugify
from product.models import Product
import datetime 

class Order(models.Model) :
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    is_completed = models.BooleanField(default = False)
    is_deliverd = models.BooleanField(default = False)
    is_paid = models.BooleanField(default = False)
    total_price = models.FloatField(default = 0)
    total_item = models.IntegerField(default = 0)
    additional = models.TextField(default = '', max_length = 3000, blank = True)
    created_at = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    deliverd_at = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    order_username = models.CharField(default = '', max_length = 100)
    order_house_no = models.IntegerField(default = 0)
    order_address = models.CharField(default = '', max_length = 200)
    order_city = models.CharField(default = '', max_length = 30)
    order_phone_number = models.CharField(default = '', max_length = 10)
    order_pin = models.IntegerField(default = 0)
    order_list = models.ImageField(upload_to='orderlist/', blank=True, null=True)
    
    def __str__(self) :
        return str(self.id) + " | " + self.user.username + " | " + str(self.created_at)[0:19] 
  
     
class OrderItem(models.Model) :
    product = models.ForeignKey(Product, on_delete = models.CASCADE, default = None)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, default = None)
    quantity = models.IntegerField(default = 1)
    price = models.FloatField(default = 0)
    item_offer = models.CharField(max_length = 1000, default = "", blank = True)
    # image = models.URLField(default = None)
    
    def __str__(self) :
        return str(self.id) + " | " + self.order.user.username + " | " + self.product.name + " | " + str(self.order.created_at)[0:19]

    def save(self, force_insert, using):
        if self.id == None :
            price = int(self.quantity) * self.product.price
            self.order.total_price = self.order.total_price + price
            self.price = price
            # self.image = self.product.image
            self.order.total_item = self.order.total_item + 1
            self.order.save()
        super().save()
