from django.db import models
from user.models import User

# Create your models here.


class PatientProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True,blank=True)
    address=models.TextField(blank=True)
    medical_history=models.TextField()
    additional_information=models.TextField()

    def __str__(self):
        return self.user.username
