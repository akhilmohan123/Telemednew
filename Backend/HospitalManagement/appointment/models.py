from django.db import models
from user.models import User
# Create your models here.

class Appointmentmodel(models.Model):
    patient=models.ForeignKey(User,related_name='patient_appointment',on_delete=models.CASCADE)
    doctor=models.ForeignKey(User,related_name='doctor_appointment',on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    note=models.CharField(max_length=20)
    status=models.CharField(max_length=20,choices=[("completed","completed"),("confirmed","confirmed"),("pending","pending")],null=True)
    def __str__(self):
        return f"{self.patient} booked {self.doctor} on {self.date} at {self.time}"
