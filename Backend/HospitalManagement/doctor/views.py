from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import DoctorCreateSerializer,GetDoctorSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from patient.authentication import JWTAuthentication
from .models import DoctorModel
from user.models import User
from . models import DoctorModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import jwt
class DoctorCreateView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = (MultiPartParser, FormParser)
    def get_object(self):
        try:
            return DoctorModel.objects.get(user=self.request.user)
        except DoctorModel.DoesNotExist:
            return None
    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        # If the instance exists, update the profile instead of creating a new one
        if instance:
            return self.update(request, *args, **kwargs)
        # Otherwise, create a new profile
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:     
            print(serializer.errors)    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
    def perform_update(self, serializer):
        serializer.save()
class GetDoctordata(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    
    def get(self,request):
        token=request.headers.get('Authorization')
        token=token.split(' ')[1]
        if not token:
            raise AuthenticationFailed("Unauthorized token")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print("Decoded payload:", payload)  # Print the decoded payload for debugging

            user = User.objects.get(id=payload['id'])
            
            try:
                doctor = DoctorModel.objects.get(user=user)
                 
                print(doctor)
                
              
            except DoctorModel.DoesNotExist:
                return Response({"error": "Patient profile not found"}, status=404)
           
            # Serialize the patient profile
            serializer = GetDoctorSerializer(doctor)
            
            print("serializer is",serializer.data)
          
    
            if not serializer.data:
                raise ValueError("No serializer data")

            return Response(serializer.data, status=200)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
        except Exception as e:
            return Response({"error": str(e)}, status=500)
