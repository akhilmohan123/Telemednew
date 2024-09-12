from django.urls import path
from . views import Appointmentview
urlpatterns = [
   path('createdoctor/<int:id>',Appointmentview.as_view(),name='createdoctor'),
]