from django.db import models
from user.models import User
class DoctorModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.TextField(default="nill", blank=True, null=True)
    license_no = models.IntegerField(blank=True, null=True)
    organization_name = models.TextField(default="nill", blank=True, null=True)
    location = models.TextField(default="nill", blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    experience = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user.username




