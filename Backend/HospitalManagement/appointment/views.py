from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AppointmentSerializers
from rest_framework.permissions import IsAuthenticated
from patient.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from . models import Appointmentmodel
# Create your views here.
class Appointmentview(APIView):
    serializer_class=AppointmentSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_queryset(self):
        user=self.request.user
        if user.is_staff():
            return Appointmentmodel.objects.all()
        elif user.hasattr(user,'user'):
            return Appointmentmodel.objects.filter(doctor=user)
        else:
            return Appointmentmodel.objects.filter(patient=user)
    def post(self,request,id):
        data=request.data.copy()
        data['doctor']=id
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
             serializer.save(patient=request.user)
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

