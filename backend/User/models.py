from .manager import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from dukandar.models import ApniDukan
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin) :
    username = models.CharField(max_length  = 100, default = "", unique = True)
    email = models.EmailField(default = "", blank = True, max_length=50)
    phone_number = models.CharField(default = "", blank = True, max_length = 10)
    first_name = models.CharField(default = "", blank = True, max_length = 50)
    last_name = models.CharField(default = "", blank = True, max_length = 50)
    city = models.CharField(default = "", blank = True, max_length = 100)
    area = models.CharField(default = "", blank = True, max_length = 500)
    house_no = models.IntegerField(default = 0)
    notifications = models.IntegerField(default = 0)
    default_dukan = models.ForeignKey(ApniDukan, on_delete = models.SET_DEFAULT, default = '1', blank = True)
    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=("Designates whether the user is super user or not."),
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def save(self, force_insert = True, using = 'my db', update_fields = []) :
        self.username = self.username.replace(' ','')
        super().save()    