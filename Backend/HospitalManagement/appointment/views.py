from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AppointmentSerializers,GetdoctorAppointmentserializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from patient.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from . models import Appointmentmodel
from doctor.models import DoctorModel
import jwt
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
# Create your views here.
class Appointmentview(APIView):
    serializer_class=AppointmentSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request,*args,**kwargs):
        user=self.request.user
        if user.is_staff:
            appointments=Appointmentmodel.objects.all()
        elif hasattr(user,'doctor'):
            appointments=Appointmentmodel.objects.filter(doctor=user)
        else:
            appointments=Appointmentmodel.objects.filter(patient=user)
        serializer=self.serializer_class(appointments,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,id):
        doctor = get_object_or_404(DoctorModel, id=id)
        print(doctor)
        data=request.data.copy()
        data['doctor']=doctor.id
        serializer=self.serializer_class(data=data)     
        if serializer.is_valid():
             serializer.save(patient=request.user)
             print(serializer.data)
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self,request,*args,**kwargs):
        instance=self.get_object()
        serializer=self.serializer_class(instance=instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteAppointment(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[JWTAuthentication]
    def delete(self,request,id):
        appointment=get_object_or_404(Appointmentmodel,id=id)
        appointment.delete()
        return Response(status=status.HTTP_200_OK)


class GetDoctorAppointment(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed("Unauthorized token")

        try:
            token = token.split(' ')[1]  # Extract the token part
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print("Decoded payload:", payload)  # Debugging
            user = User.objects.get(id=payload['id'])

            # Fetch appointments for the doctor
            appointments = Appointmentmodel.objects.filter(doctor=user)
           
            print(appointments)
            if not appointments.exists():
                return Response({"message": "No appointments found"}, status=404)

            serializer = GetdoctorAppointmentserializer(appointments, many=True)
           
            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
