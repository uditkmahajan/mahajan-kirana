from django.db import models
from User.models import User


# Create your models here.

class AppReview(models.Model): 
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    rating = models.IntegerField(default = 5)
    comment = models.CharField(default = "", max_length=1000)
    
    def __str__(self) :
        return str(self.rating) + " start | " + " by " + self.user.username    
    
class AppFeedback(models.Model): 
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    feedback = models.CharField(default = "", max_length=1000)

    def __str__(self) :
        return self.user.username
    
class Notification(models.Model) :
    title = models.CharField(default = '', max_length = 100)
    date = models.DateTimeField(auto_now_add = True)
    notification = models.TextField(default = '', max_length = 4000)
    
    def __str__(self) :
        return self.title
    
    
    