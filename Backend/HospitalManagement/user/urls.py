
from django.urls import path
from . views import RegistrationView,LoginView,UserView,LogoutView
urlpatterns = [
   path('register',RegistrationView.as_view(),name='register'),
   path('login',LoginView.as_view(),name='login'),
   path('user',UserView.as_view(),name='user'),
   path('logout',LogoutView.as_view(),name='logout')
  
]