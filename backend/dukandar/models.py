from django.db import models
from django.core.files.storage import default_storage

# Create your models here.
class ApniDukan(models.Model) :
    name = models.CharField(max_length = 200)
    owner = models.CharField(max_length = 200)
    slug = models.CharField(max_length = 500, blank = True)
    area = models.CharField(max_length = 200)
    about = models.CharField(max_length = 1000, blank = True)
    delivery_detail = models.TextField(max_length = 2000, blank = True)
    phone_number = models.CharField(max_length = 10, blank = True)
    whatsapp_number = models.CharField(max_length = 10, blank = True)
    owner_image = models.ImageField(upload_to='apnidukan/dukanowner/')
    banner_image = models.ImageField(upload_to='apnidukan/dukanbanner/')
    is_active = models.BooleanField(default = True)
    
    def save(self, *args, **kwargs) :
        self.slug = self.name.replace(' ', '-') + '-' + self.area
        super().save(*args, **kwargs)

    def __str__(self) :
            return self.name
    
    
#  new_slug = self.name.replace(' ', '-') + '-' + self.area
#         new_owner_image = self.owner_image
#         new_banner_image = self.banner_image
#         try:
#                 old_instance = ApniDukan.objects.get(pk=self.pk)
#                 old_owner_image = old_instance.owner_image
#                 old_banner_image = old_instance.banner_image
#                 old_slug = old_instance.slug
#         except ApniDukan.DoesNotExist:
#                 old_owner_image = None
#                 old_banner_image = None
#                 old_slug = None
#         print('old => ', old_owner_image, old_banner_image, 'new => ', new_owner_image, new_banner_image, 'id => ',self.id, 'slug => ',old_slug, new_slug)
#         if old_owner_image and new_owner_image and (old_owner_image != new_owner_image or (old_owner_image == new_owner_image and old_slug != new_slug)) :
#                 if default_storage.exists(old_owner_image.name):
#                     print(old_owner_image.name)
#                     default_storage.delete(old_owner_image.name)
#         if old_banner_image and new_banner_image and (old_banner_image != new_banner_image or (old_banner_image == new_banner_image and old_slug != new_slug)):
#                 if default_storage.exists(old_banner_image.name):
#                     default_storage.delete(old_banner_image.name)
#         # if self.id != None : 
#         print(self.id, self.slug)
#         self.owner_image.name = 'apnidukan/dukanowner/' + self.slug + '-owner-image.jpg'
#         # self.owner_image.url = 'apnidukan/dukanowner/' + self.slug + '-owner-image.jpg'
#         self.banner_image.name = 'apnidukan/dukanbanner/' + self.slug + '-banner-image.jpg'
#         # else :
#         #         self.owner_image.name =  self.slug + '-owner-image.jpg'
#         #         self.banner_image.name = self.slug + '-banner-image.jpg'