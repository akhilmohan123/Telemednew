from django.db import models
from user.models import User
import os
def get_image_upload_path(instance, filename):
    # Ensure the user object is loaded
    user_id = instance.user.id if instance.user else 'unknown'
    # Define the path format
    return os.path.join('image', f'{user_id}_{filename}')
class DoctorModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.TextField(default="nill", blank=True, null=True)
    license_no = models.IntegerField(blank=True, null=True)
    organization_name = models.TextField(default="nill", blank=True, null=True)
    location = models.TextField(default="nill", blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True,max_length=12)
    experiance = models.IntegerField(default=0, null=True)
    available_status=models.TextField(null=True)
    image=models.ImageField(upload_to='image/',default='default_images/default_avatar.png')

    unique_together=("doctor","date","time")

    def __str__(self):
        return self.user.email




