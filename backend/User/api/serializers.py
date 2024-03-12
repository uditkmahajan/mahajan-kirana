from User.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer): 
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    class Meta :
        model = User
        exclude = ('groups', 'user_permissions', 'id')
        extra_kwargs = {
            'password' : {
                'write_only' : True,
            },
            'last_login' : {
                'write_only' : True,
            },
        }
      
    def validate_phone_number(self, phone_number) :
        try :
            if len(phone_number) == 10 and int(phone_number):
                return phone_number 
            raise serializers.ValidationError('Phone Number must contain 10 digits')
        except Exception as e :
            raise serializers.ValidationError('Phone Number must contain only numbers')
    
    
    def validate_password(self, password) : 
        if len(password) >= 6 :
            return password
        raise serializers.ValidationError('Password must contain minimum 6 digits')
    
    
    def create(self, validated_data) :
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
