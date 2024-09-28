from rest_framework import serializers
from .models import Appointmentmodel,Medicine
from user.models import User
from doctor.models import DoctorModel
from patient.models import PatientProfile
class AppointmentSerializers(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
      model=Appointmentmodel
      fields=["id","doctor","doctor_name","date","time","note","referrence_no","refer_doctor","status"]
      read_only_fields=["patient","status"]
    def get_doctor_name(self, obj):
        try:
            # Get the related doctor object from the Appointmentmodel's doctor field
            doctor = DoctorModel.objects.get(id=obj.doctor.id)  # Assuming the doctor field is a ForeignKey to DoctorModel
            user = doctor.user  # Fetch the related User object
            return f"{user.first_name} {user.last_name}"
        except DoctorModel.DoesNotExist:
            return "Doctor not found"
    def validate(self,data):
        date=data.get("date")
        time=data.get("time")
        doctor=data.get("doctor")
        if Appointmentmodel.objects.filter(date=date,time=time,doctor=doctor).exists():
            raise serializers.ValidationError("There is an Appointment for specefic date")

        return data
class GetdoctorAppointmentserializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    patient_name=serializers.SerializerMethodField()

    class Meta:
        model = Appointmentmodel
        fields = ["id","patient", "date", "time", "note", "doctor_name", "status","patient_name","referrence_no"]

    def get_doctor_name(self, obj):
        user = obj.doctor  # doctor is a User
        return f"{user.first_name} {user.last_name}"
    def get_patient_name(self,obj):
        user=obj.patient
        useris=User.objects.get(email=user)
        return f"{useris.first_name} {useris.last_name}"
class GetspeceficSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    patient_name=serializers.SerializerMethodField()
    medical_history=serializers.SerializerMethodField()
    class Meta:
        model=Appointmentmodel
        fields=["id","patient", "date", "time", "note", "doctor_name", "status","patient_name","medical_history","refer_doctor"]
    def get_doctor_name(self, obj):
        user = obj.doctor  # doctor is a User
        return f"{user.first_name} {user.last_name}"
    def get_patient_name(self,obj):
        user=obj.patient
        useris=User.objects.get(email=user)
        return f"{useris.first_name} {useris.last_name}"
    def get_medical_history(self,obj):
       try:
          user=obj.patient
          useris=PatientProfile.objects.get(user=user)
          return f"{useris.medical_history}"
       except:
           return "No Medical history"
class EditPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointmentmodel
        fields="__all__"
class AddMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medicine
        fields="__all__"
    def create(self,validated_data):
       
        data=Medicine.objects.create(**validated_data)
        
        return data
class GetMedicineSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    date=serializers.SerializerMethodField()
    class Meta:
        model=Medicine
        fields=["name","doctor_name","dosage","frequency","duration","additional_notes","date"]
    def get_doctor_name(self, obj):
        # Access the related appointment and get the doctor's name from the User model via Doctor
        print(obj.appointment.doctor)
        user_name=User.objects.get(email=obj.appointment.doctor)
        if user_name:
            return f"{user_name.first_name} {user_name.last_name}"
        return None
    def get_date(self,obj):
        print(obj.appointment.date)
        return obj.appointment.date
class GetSpeceficMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medicine
        fields='__all__'
class GetReferAppointmentSerializer(serializers.ModelSerializer):
    doctor_name=serializers.SerializerMethodField()
    refer_doctor_name=serializers.SerializerMethodField()
    special=serializers.SerializerMethodField()
    class Meta:
        model=Appointmentmodel
        fields=["id","doctor_name","date","time","note","refer_doctor_name","special","refer_doctor"]
    def get_doctor_name(self,obj):
        try:
            # Get the related doctor object from the Appointmentmodel's doctor field
            doctor = DoctorModel.objects.get(id=obj.doctor.id)  # Assuming the doctor field is a ForeignKey to DoctorModel
            user = doctor.user  # Fetch the related User object
            return f"{user.first_name} {user.last_name}"
        except DoctorModel.DoesNotExist:
            return "Doctor not found"
    def get_refer_doctor_name(self,obj):
        print(obj.refer_doctor.id)
        doctor=DoctorModel.objects.get(id=obj.refer_doctor.id)
        Refer_Doctor=f"{doctor.user.first_name} {doctor.user.last_name}"
        return Refer_Doctor
    def get_special(self,obj):
        doctor=DoctorModel.objects.get(id=obj.refer_doctor.id)
        return doctor.speciality