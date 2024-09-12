from django.urls import path
from . views import Appointmentview
urlpatterns = [
   path('createdoctor',Appointmentview.as_view(),name='createdoctor'),
]