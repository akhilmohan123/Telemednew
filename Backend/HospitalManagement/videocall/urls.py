from django.urls import path
from .views import Video_Call_View

urlpatterns=[
    path('videocall',Video_Call_View,name='videocall')
]