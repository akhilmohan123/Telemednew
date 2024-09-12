from rest_framework import serializers
from .models import Appointmentmodel
class AppointmentSerializers(serializers.ModelSerializer):
    model=Appointmentmodel
    fields=["doctor","date","time","note"]
    read_only=["patient","status"]
    def validate(self,data):
        date=data.get("date")
        time=data.get("time")
        doctor=data.get("doctor")
        if Appointmentmodel.objects.filter(date=date,time=time,doctor=doctor).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("There is an Appointment for specefic date")
    
        return data
          
           
