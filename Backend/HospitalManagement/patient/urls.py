from django.urls import path
from . views import PatientProfileCreateUpdateView,GetprofilePatient
urlpatterns = [
   path('addprofile',PatientProfileCreateUpdateView.as_view(),name='addprofile'),
   path('getprofile',GetprofilePatient.as_view(),name='getprofile')
]