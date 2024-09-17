from django.urls import path
from . views import Appointmentview,DeleteAppointment,GetDoctorAppointment,GetSpeceficPatient,EditDoctorView
urlpatterns = [
   path('appointments',Appointmentview.as_view(),name='createdoctor'),
   path('createdoctor/<int:id>',Appointmentview.as_view(),name='createdoctor'),
   path('appointmentdelete/<int:id>',DeleteAppointment.as_view(),name='appointmentdelete') ,
   path('getdoctor-appointments',GetDoctorAppointment.as_view(),name='getdoctor-appointments'),
   path('getspecefic/<int:id>',GetSpeceficPatient.as_view(),name='getspecefic'),
   path('edit-patient/<int:id>',EditDoctorView.as_view(),name='edit-doctor')
]
