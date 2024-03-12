from django.db import models
from User.models import User
from django.utils.text import slugify
from django.core.files.storage import default_storage
from dukandar.models import ApniDukan
# Create your models here.


class Category(models.Model):
    name = models.CharField(default = '', max_length = 400)
    slug = models.SlugField(default = '', max_length = 400, blank = True)
    image = models.ImageField(upload_to = 'category/', default = 'category/download.jpeg')
    total_products = models.IntegerField(default = 0)
    
    def save(self) :
        self.slug = slugify(self.name)
        super().save()

    def __str__(self) :
        return self.name
 
 
class Product(models.Model) :
    dukan = models.ForeignKey(ApniDukan, on_delete = models.CASCADE, default = '1')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default = None, related_name = 'products')
    name = models.CharField(default = '', max_length = 300)
    slug = models.CharField(default = '', max_length = 300, blank = True)
    image = models.ImageField(upload_to='products/', blank=True)
    url = models.CharField(blank = True, max_length = 1000)
    description = models.CharField(max_length=1000, default = '', blank = True)
    avg_rating = models.FloatField(default = 0)
    total_reviews = models.IntegerField(default = 0)
    mrp = models.IntegerField(default = 0)
    price = models.FloatField()
    discount = models.FloatField(default = 0)
    is_active = models.BooleanField(default = True)
    offer = models.CharField(max_length = 1000, default = "", blank = True)
    
    def save(self) :
        self.slug = slugify(self.name)
        if self.mrp == 0 : 
            self.mrp = self.price
        self.discount = round(((self.mrp - self.price) * 100 ) / self.mrp, 1)
        if self.id == None: 
            self.category.total_products = self.category.total_products + 1
            self.category.save()
        super().save()
        
    def __str__(self) :
        return self.name
    
    
class Review(models.Model) :
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, default = None)
    rating = models.IntegerField(default = 1)
    comment = models.CharField(default = '', max_length=1000)
    
    def save(self, force_insert = True, using = 'my db') :
        if self.id == None : 
            total_reviews = self.product.total_reviews + 1
            self.product.avg_rating = round(((self.product.avg_rating * self.product.total_reviews) + self.rating) / total_reviews,1)
            self.product.total_reviews = total_reviews
            self.product.save()
        super().save()
    
    
    def __str__(self) :
        return str(self.rating) + ' start | ' + self.product.name + ' by ' + self.user.username
    
    
#  new_image = self.image
#         try:
#                 old_instance = Product.objects.get(pk=self.pk)
#                 old_image = old_instance.image
#         except Product.DoesNotExist:
#                 old_image = None
#         if old_image and new_image and old_image != new_image:
#                 if default_storage.exists(old_image.name):
#                     default_storage.delete(old_image.name)
#         self.image.name = 'product/' + self.slug + "-image.jpg"