from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import RegisterSerializer,LoginSerializer,UserSerializer
from . models import User
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

import jwt,datetime
class RegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        print(request.data)
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):  
        print("login view called")
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data
        user=User.objects.get(id=user.id)
        userjson=UserSerializer(user)
        print(userjson.data)
        
        payload={
            'id': user.id,
            'exp': timezone.now() + datetime.timedelta(minutes=60),  # Expiration timeth
            'iat': timezone.now()  # Issued at time
        }
        token=jwt.encode(payload,'secret',algorithm='HS256').encode('utf-8')
        response=Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token,
            'user':userjson.data
        }
        return response
class UserView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
       
        token = token.split(' ')[1]
        print("Received token:", token)
        
        # Print the token for debugging
        
        if not token:
            raise AuthenticationFailed("Unauthenticated: Token not found")

        try: 
            # Decode the JWT token
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print("Decoded payload:", payload)  # Print the decoded payload for debugging

            # Retrieve user based on the payload data
            user = User.objects.get(id=payload['id'])  # Ensure 'id' is the correct field
            
            # Serialize the user data
            serializer = UserSerializer(user)
            
            return Response(serializer.data)
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
        except Exception as e:
            # Catch any other exceptions and log them
            print(f"An error occurred: {e}")
            raise AuthenticationFailed("An error occurred while processing your request")
class LogoutView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        response=Response({
            "message":"Logoutsuccessfully"
        })
        response.delete_cookie("jwt")
        return response