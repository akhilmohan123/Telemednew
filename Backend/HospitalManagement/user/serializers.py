from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from . models import User
import bcrypt

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        extra_kwargs = {'password': {'write_only': True}}
    def create(self,validated_data):
        user=User(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'],
                role=validated_data['role']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user
class LoginSerializer(serializers.Serializer):
        print("serializer called")
        email = serializers.CharField(max_length=255)
        password=serializers.CharField(write_only=True)
        def validate(self,data):
            email=data.get('email')
            password=data.get('password')
            user=User.objects.filter(email=email).first()
            print(f"User's hashed password: {user.password}")
            print(f"Password check result: {user.check_password(password)}")
            
            if user is None:
               raise AuthenticationFailed('User Not found')
            if not user.check_password(password):
               raise AuthenticationFailed(password)
           
            return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'