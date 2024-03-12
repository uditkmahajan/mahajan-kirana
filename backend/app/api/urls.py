from django.contrib import admin
from django.urls import path, include
from .views import AppReviewView, AppFeedbackView, NotificationView, IsReviewdView

urlpatterns = [
    path('reviews/',AppReviewView.as_view({
        'get' : 'getReviews',
        'post' : 'createReview'
    }), name = 'get all the reviews of the website and create a review'),
    
    path('isReviewd/', IsReviewdView.as_view({
        'get' : 'getIsReviewd'
    }), name = 'get a user is reviewd or not'),
    
    path('feedback/', AppFeedbackView.as_view({
        'post' : 'createFeedback'
    }), name = 'create a feedback for the website') ,
    
    path('notification/', NotificationView.as_view({
        'get' : 'getNotifications'
    }), name = 'get all the notifications')
]
