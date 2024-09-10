from rest_framework import serializers
from .models import DoctorModel
class DoctorCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model=DoctorModel
        fields = ['speciality', 'license_no', 'organization_name', 'location', 'phone_number', 'experience']
     def create(self, validated_data):
        # We don't need to handle user here, it's done in the view.
             profile = DoctorModel.objects.create(**validated_data)
             return profile

     def update(self, instance, validated_data):
        # No need to handle user here, it's handled by the view.
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()
            return instance
class GetDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields="__all__"