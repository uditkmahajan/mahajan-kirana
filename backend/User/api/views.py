from User.models import User
from product.models import Product
from order.models import Order
from app.models import Notification, AppReview
from dukandar.models import ApniDukan
from .serializers import UserSerializer
from dukandar.api.serializers import ApniDukanSerializer
from product.api.serializers import ProductSerializer
from .throttling import AnnonThrottle, UserThrottle
from django.contrib.auth import authenticate
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import Throttled
from rest_framework.permissions import IsAuthenticated
import yagmail
import random
import keyring

# convert the time for the limit reached 
def time_convert(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


# get access and refresh token for the user
def get_access_refresh_token(username) :
    refresh = RefreshToken.for_user(User.objects.get(username = username))
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return refresh_token, access_token


# return the serializer.errors in the form - field : error message
def validation_error(serializer) : 
    for i,j in serializer.errors.items() :
            value = j[0]
            key = i 
    return key + ' : ' + value
    

# create and login view   - checked
class UserCreateLoginView(ViewSet) : 
    throttle_classes = [AnnonThrottle]
    
    # throttling message 
    def throttled(self, request, wait):
        raise Throttled(
            detail={
                'message': f'Request Limit Exceeded. Please Wait {time_convert(wait)} and Try again.'
            }
        )

    # function for creating a new user
    def createUser(self, request) :
        print('createUser request.data => ', request.data)
        try :
            request.data['username'] and request.data['password'] and request.data['email'] 
            request.data['username'] = request.data.get('username').replace(' ', '')
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid() :
                serializer.save()
                refresh_token, access_token = get_access_refresh_token(request.data['username'])
                return Response({'access_token': access_token, 'success' : True})
            return Response({'error_message' : validation_error(serializer)})
        except Exception as e :
            print('createUser exception => ', e)
            return Response({'error_message' : 'All the fields are required!'})   
    
    # function for logging a user
    def loginUser(self, request) :
        print('loginUser request.data => ', request.data)
        try :
            request.data['username'] and request.data['password'] 
            if authenticate(username = request.data['username'], password = str(request.data.get('password'))) != None :
                refresh_token, access_token = get_access_refresh_token(request.data['username'])
                return Response({'success' : True, 'access_token' : access_token})
            else : 
                return Response({'error_message' : 'Invalid username or password!'})  
        except Exception as e :
            print('loginUser exception => ',e)  
            return Response({'error_message' : 'All the fields are requeired!'})


# update delete retriev view - checked
class UserView(ViewSet): 
    permission_classes = [IsAuthenticated] 
    
    # get the use data - complete profile
    def getUser(self, request, username) :
        try : 
            if username == request.user.username : 
                user = User.objects.get(username=request.user.username)
                serializer = UserSerializer(user)
                return Response({'success' : 'Profile', 'data' : serializer.data})
            return Response({'error_message' : 'Invalid username!'})
        except Exception as e :
            print('getUser exception => ', e)
            return Response({'error_message' : 'Network Error'})
        
    # update the user data
    def updateUser(self, request, username) :
        print('updateUser request.data => ',request.data)
        try : 
            if username == request.user.username : 
                user = User.objects.get(username=request.user.username)
                serializer = UserSerializer(user , data = request.data, partial = True)
                if serializer.is_valid() :
                    serializer.save()
                    return Response({'success' : 'Data updated', 'data' :serializer.data}) 
                return Response({'error_message' : validation_error(serializer)})
            return Response({'error_message' : 'Invalid username!'})  
        except Exception as e :
            print('updateUser exception => ', e)
            return Response({'error_message' : 'Internal Error'})
    
    # delete the user data
    def deleteUser(self, request, username) :
        if username == request.user.username : 
            user = User.objects.get(username=request.user.username)
            user.delete()
            return Response({"success" : True})
        return Response({"error_message" : "Invalid username!"})

                  
# forgot password - checked
class ForgotPasswordView(ViewSet) :
    throttle_classes = [AnnonThrottle]
    
    # throttling message 
    def throttled(self, request, wait):
        raise Throttled(
            detail={
                'message': f'Request Limit Exceeded. Please Wait {time_convert(wait)} and Try again.'
            }
        )
        
    def forgotPassword(self, request) :
        print('forgotPassword request.data => ', request.data)
        if request.data.get('username') and request.data.get('email') :
            service_name = "yagmail"  # The service name you used while saving the password
            keyring.set_password(service_name, 'mahajankiranamhs@gmail.com', 'cggnprpnonhhhbgu')
            password = ''.join(random.choice(['a','b','c','d','e', 'z', 'h', 'm', 's', '8', '1', '2', '3', '7', '9', '#', '%', '&', '@', '$']) for _ in range(6)) 
            try :
                user = User.objects.get(username = request.data['username'])
                if user.email == request.data['email'] :
                    sender_email = 'mahajankiranamhs@gmail.com'
                    receiver_email = request.data['email']
                    subject = 'Password Recovery'
                    html_message = f'''<h2>Namaste 🙏 {request.data['username']},</h2>
                                        <h4>Your new password for the Mahajan Kirana is - </h4> <h3 style='color : red; background-color : yellow; display : inline;'>{password}</h3>                                      
                                        <h4> Please login with new password ! <h4> 
                                        <a href='http://localhost:3000/user/loginUser/' style="font-size : 10px; color: red; border: 1px solid red; padding: 2px 10px; border-radius: 20px; background-color: #ff000021;" target='_blank'>Login</a>
                                        <h1 style='font-size : 13px'>To change password go to <a href='http://localhost:3000/user/udit/profile/' target='_blank' style="color : red"> profile</a></h1>
                                        <h5 style='color: blue'>With Love from Mahajan Kirana !</h5>
                                        '''
                   
                   
                   
                    yag = yagmail.SMTP(sender_email)
                    yag.send( to=receiver_email, subject=subject, contents=[html_message])
                    yag.close()
                    user.set_password(password)
                    user.save()
                    return Response({"success" : True})
                else :
                    return Response({'error_message' : 'Incorrect email!'})
            except Exception as e :
                print('forgotPassword exception => ', e)
                if "Emailaddress" in str(e) :
                    return Response({"error_message" : 'Incorrect email!'})
                elif str(e) == 'User matching query does not exist.' :
                    return Response({'error_message' : 'Incorrect username!'})
                return Response({'error_message' :'Unable to send email!'})
        else :
            return Response({'error_message' : 'All the fields are required!'})
        
     
# create a new password - checked
class ResetPasswordView(ViewSet) :
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserThrottle]
    
    # throttling message 
    def throttled(self, request, wait):
        raise Throttled(
            detail={
                'message': f'Request Limit Exceeded. Please Wait {time_convert(wait)} and Try again.'
            }
        )
        
    # reset the old password 
    def resetPassword(self, request) :
        print('resetPassword request.data => ', request.data)
        try :
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            if old_password == None or new_password == None :
                return Response({'error_message' : 'All the fields are required!'})
            if len(new_password) >= 6 :
                if authenticate(username = request.user.username, password = old_password) != None : 
                    user = User.objects.get(username = request.user.username) 
                    user.set_password(new_password)
                    user.save()
                    return Response({'success' : 'Password has been reset!'})
                else :
                    return Response({'error_message' : 'Incorrect password!'})
            else :
                return Response({'error_message' : 'New password must contain 6 characters!'}) 
        except Exception as e :
            print('resetPassword exception => ', e)
            return Response({'error_message' : 'Internal Error'})
   
   
# get the user information - checked
class UserInfoView(ViewSet) :
    permission_classes = [IsAuthenticated]
    
    def userInfo(self, request) :
        print('userInfo request.data => ', request.data)
        try : 
            user = User.objects.get(username = request.user.username)
            total_customer =  len(User.objects.all()) 
            total_order = len(Order.objects.all())
            product = Product.objects.all() 
            top_discount_product = ProductSerializer(Product.objects.filter(discount__gte = 5).order_by('-discount'), many = True)
            total_product = len(product)
            product_list = [i.name for i in product]  
            reviews = AppReview.objects.all() 
            total_item = 0
            avg_rating = 0
            if len(reviews) != 0 :
                for i in reviews :
                      avg_rating = i.rating + avg_rating
                avg_rating = round(avg_rating / len(reviews), 1)
            notification = len(Notification.objects.all()) - user.notifications
            if notification <= 0 :
                notification = 0
            if Order.objects.filter(user = user.id, is_completed = False).exists() :
                total_item = Order.objects.get(user = user.id, is_completed = False).total_item 
            return Response({'user' : user.username, 'default_dukan' : str(user.default_dukan.slug), 'total_item' : total_item, 'notification' : notification, 'product_list' : product_list, 'total_reviews' : len(reviews), 'avg_rating' : avg_rating, 'total_customer' : total_customer, 'total_product' : total_product, 'total_order' : total_order, 'top_discount_product' : top_discount_product.data})
        except Exception as e :
            print('userInfo exception => ',e)
            return Response({'error_message' : 'Unable to get the userInfo!'})
  
  
#  get the basic information  - checked
class BasicInfoView(ViewSet) :   
     
    def basicInfo(self, request) : 
        total_customer =  len(User.objects.all()) 
        total_order = len(Order.objects.all())
        product = Product.objects.all() 
        top_discount_product = ProductSerializer(Product.objects.filter(discount__gte = 5).order_by('-discount'), many = True)
        total_product = len(product)
        product_list = [i.name for i in product]  
        reviews = AppReview.objects.all() 
        avg_rating = 0
        if len(reviews) != 0 :
            for i in reviews :
                avg_rating = i.rating + avg_rating
            avg_rating = round(avg_rating / len(reviews), 1)
        notification = len(Notification.objects.all())
        return Response({'product_list' : product_list, 'notification' : notification, 'total_reviews' : len(reviews), 'avg_rating' : avg_rating, 'total_customer' : total_customer, 'total_product' : total_product, 'total_order' : total_order, 'top_discount_product' : top_discount_product.data})
      
        
class ApniDukanView(ViewSet) :
    permission_classes = [IsAuthenticated]
    
    def apniDukan(self, request) :
        print('apniDukan query params => ', request.query_params)
        try : 
            apni_dukan = ApniDukan.objects.filter(slug = request.query_params.get('apniDukan')).first()
            if request.query_params.get('set') == 'true' :
                user = User.objects.get(id = request.user.id)
                user.default_dukan = apni_dukan
                user.save()
            serializer = ApniDukanSerializer(apni_dukan)
            return Response({'data' : serializer.data})
        except Exception as e :
            print('apniDukan exception => ',e)
            return Response({'error_message ' : 'Not Found!'})
    
    def allDukan(self, request) :
        allDukan = [] 
        for i in ApniDukan.objects.all() :
            allDukan.append(i.slug)
        return Response({'data' : allDukan})
    
    
    
    
    
    
    
    
    
    
#   <div style="border : 1px solid rgba(128, 128, 128, 0.208); padding : 20px; display : flex; flex-direction: column; align-items :center; gap : 5px; max-width : 600px; margin : auto">
#                                             <h4 style="color: red;">MahajanKirana</h4>
#                                             <h6 style="font-size: 15px;">Password Recovery Mail</h6>
#                                             <h6 style="font-size: 15px;">for user - <span style="color: red;">{request.data['username']}</span></h6>
#                                             <hr style="margin-top: 1px; margin-bottom : 1px"/>
#                                             <h6 style="font-size: 15px;">Your new password for MahajanKirana is -</h6>
#                                             <h5 style="color: red;">{password}</h5>
#                                             <h6 style="font-size: 15px;">Please login with this new password !</h6>
#                                             <a href='http://localhost:3000/user/loginUser/' style="color: red; border: 1px solid red; padding: 2px 10px; border-radius: 20px; background-color: #ff000021;" target='_blank'>Login</a>
#                                             <h1 style='font-size : 13px'>To change password go to <a href='http://localhost:3000/user/udit/profile/' target='_blank' style="color : red"> profile</a></h1>
#                                         </div>