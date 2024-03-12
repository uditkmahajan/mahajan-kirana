from .views import UserCreateLoginView, UserView, ForgotPasswordView, UserInfoView, BasicInfoView, ResetPasswordView, ApniDukanView
from django.urls import path

urlpatterns = [
    path('createUser/', UserCreateLoginView.as_view({
            'post' : 'createUser'
    }), name = 'create a user'),
    
    path('loginUser/', UserCreateLoginView.as_view({
            'post' : 'loginUser'
    }), name = " logint a user"),
    
     path('forgotPassword/', ForgotPasswordView.as_view({
            'post' : 'forgotPassword'
    }), name = 'forgot password'),
    
    path('userInfo/', UserInfoView.as_view({
            'get' : 'userInfo'
    }), name = 'get the neseccary user information' ),
       
    path('basicInfo/', BasicInfoView.as_view({
            'get' : 'basicInfo'
    }), name = 'get all the basic info'),
    
    path('resetPassword/', ResetPasswordView.as_view({
            'post' : 'resetPassword'
    }), name = 'to change the old password'),
    
    path('apniDukan/', ApniDukanView.as_view({
            'get' : 'apniDukan'
    })),
    
    path('allDukan/', ApniDukanView.as_view({
            'get' : 'allDukan'
    })),
    
    path('<str:username>/', UserView.as_view({
            'get' : 'getUser',
            'put' : 'updateUser',
            'delete' : 'deleteUser'
    }), name = 'get update delete the user'),
] 
