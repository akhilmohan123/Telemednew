from django.urls import path
from . views import Appointmentview,DeleteAppointment,GetDoctorAppointment,GetSpeceficPatient,EditDoctorView,AddMedicineViews,GetMedicineView,GetSpeceficMedicine,GetReferAppointment
urlpatterns = [
   path('appointments',Appointmentview.as_view(),name='createdoctor'),
   path('createdoctor/<int:id>',Appointmentview.as_view(),name='createdoctor'),
   path('appointmentdelete/<int:id>',DeleteAppointment.as_view(),name='appointmentdelete') ,
   path('getdoctor-appointments',GetDoctorAppointment.as_view(),name='getdoctor-appointments'),
   path('getspecefic/<int:id>',GetSpeceficPatient.as_view(),name='getspecefic'),
   path('edit-patient/<int:id>',EditDoctorView.as_view(),name='edit-doctor'),
   path('add-medicine',AddMedicineViews.as_view(),name='add-medicine'),
   path('get-medicines',GetMedicineView.as_view(),name='get-medicine'),
   path('specefic-medicine/<int:id>',GetSpeceficMedicine.as_view(),name='get-specefic'),
   path('get-refer-appointments',GetReferAppointment.as_view(),name='get-refer-appointments')
]
