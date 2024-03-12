from app.models import AppReview, Notification
from User.models import User
from .serializers import AppReviewSerializer, AppFeedbackSerializer, NotificationSerializer
from .pagination import AppReviewPagination
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# return the serializer.errors
def validation_error(serializer) : 
    for i,j in serializer.errors.items() :
            value = j[0]
            key = i 
    return key + ' : ' + value


# get the data after pagination
def get_paginated_data(self, serializer, data) :
    serializer = serializer(data, many = True)
    data = self.paginate_queryset(serializer.data)
    result = self.get_paginated_response(data).data
    return result


# app review view - checked
class AppReviewView(ListAPIView, ViewSet) :
    
    # get all the reviews for the website
    def getReviews(self, request) :
        t = 0
        reviews = AppReview.objects.all().order_by('-rating', '-id')
        if len(reviews) == 0 :
            return Response({'error_message' : 'No reviews!', 'is_reviewd' : False})
        elif len(reviews) > 20 :
            t = 20
        else :
            t = len(reviews)
        serializer = AppReviewSerializer(reviews[0:t], many = True)
        return Response({'data' : serializer.data})
    
    # create the review for the app
    def createReview(self, request) :
        print('createReview request.data => ', request.data)
        try :
            AppReview.objects.get(user = request.user.id)
            return Response({"error_message" : "User already reviewed!"})
        except Exception as e :
            print('createReview exception => ', e)
            request.data['user'] = request.user.id
            serializer = AppReviewSerializer(data= request.data)
            if serializer.is_valid() :
                serializer.save()
                return Response({"success" : True})
            return Response({"error_message" : validation_error(serializer)})

            

# checks user reviewd or not - checked
class IsReviewdView(ViewSet) :
    
    def getIsReviewd(self, request) :
        reviewd = True
        try : 
            print('review or not => ',AppReview.objects.get(user = request.user.id))
        except Exception as e :
            print('IsReviewd exception =>',e)
            reviewd = False
        return Response({'is_reviewd' : reviewd})
   
    
  
#  feedback view
class AppFeedbackView(ViewSet) :
    permission_classes = [IsAuthenticated]
    
    # create the feedback for the app
    def createFeedback(self, request) :
        print('createFeedback request.data = > ',request.data)
        try : 
            request.data['user'] = request.user.id
            serializer = AppFeedbackSerializer(data = request.data)
            if serializer.is_valid() :
                serializer.save()
                return Response({"success" : True})
            return Response({"error_message" : validation_error(serializer)})
        except Exception as e :
            print('createFeedback exception = > ',e)
            return Response({'data' : e})
    
    
    
# notification view
class NotificationView(ViewSet) :

    # get all the notifications
    def getNotifications(self, request) :
        print('getNotifications requeset.query_params => ', request.query_params)
        notifications = Notification.objects.all().order_by('-date')
        try : 
            user = request.query_params['user']
            user = User.objects.get(username = user)
            user.notifications = len(notifications)
            user.save()
        except Exception as e :
            print('getNotifications exception => ',e)
        if len(notifications) == 0 :
            return Response({'error_message' : 'No Notifications!'})
        serializer = NotificationSerializer(notifications, many = True)
        return Response({'data' : serializer.data})
        