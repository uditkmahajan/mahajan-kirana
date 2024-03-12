from app.models import AppReview, AppFeedback, Notification
from rest_framework import serializers


class AppReviewSerializer(serializers.ModelSerializer) :
    username = serializers.SerializerMethodField(read_only = True)
    class Meta :
        model = AppReview
        exclude = ['id']
        extra_kwargs = {
            'user' :{
                'write_only' : True
            }
        }
        
    def get_username(self, obj) :
        return obj.user.username


class AppFeedbackSerializer(serializers.ModelSerializer) :
    class Meta :
        model = AppFeedback
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Notification
        fields = '__all__'