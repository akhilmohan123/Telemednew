from rest_framework import serializers
from .models import Appointmentmodel
class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
      model=Appointmentmodel
      fields=["doctor","date","time","note"]
      read_only=["patient","status"]
    def validate(self,data):
        date=data.get("date")
        time=data.get("time")
        doctor=data.get("doctor")
        if Appointmentmodel.objects.filter(date=date,time=time,doctor=doctor).exists():
            raise serializers.ValidationError("There is an Appointment for specefic date")
    
        return data
          
           
