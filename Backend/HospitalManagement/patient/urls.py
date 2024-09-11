from django.urls import path
from . views import PatientProfileCreateUpdateView,GetprofilePatient,GetAllDoctors
urlpatterns = [
   path('addprofile',PatientProfileCreateUpdateView.as_view(),name='addprofile'),
   path('getprofile',GetprofilePatient.as_view(),name='getprofile'),
   path('getalldoctors',GetAllDoctors.as_view(),name='getalldoctors')
]