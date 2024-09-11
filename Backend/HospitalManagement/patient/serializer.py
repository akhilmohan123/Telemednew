from rest_framework import serializers
from .models import PatientProfile
from user.serializers import UserSerializer
from doctor.models import DoctorModel
class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        # We don't need to handle user here, it's done in the view.
        profile = PatientProfile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        # No need to handle user here, it's handled by the view.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
class GetPatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields=['phone_number','date_of_birth','address','medical_history','additional_information']
class GetAllDoctorsSerializers(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    first_name=serializers.CharField(source='user.first_name',read_only=True)
    last_name=serializers.CharField(source='user.last_name',read_only=True)

    class Meta:
        model=DoctorModel
        fields = ['id', 'speciality', 'license_no', 'organization_name', 'location', 'phone_number', 'experiance', 'available_status', 'image', 'user_email','first_name','last_name']