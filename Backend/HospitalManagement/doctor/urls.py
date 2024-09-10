from django.urls import path
from . views import DoctorCreateView,GetDoctordata
urlpatterns = [
   path('createdoctor',DoctorCreateView.as_view(),name='createdoctor'),
   path('getdoctor',GetDoctordata.as_view(),name='getdoctor')
]