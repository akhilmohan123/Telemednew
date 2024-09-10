from django.contrib import admin
from . models import User
# Register your models here


class AdminAuth(admin.ModelAdmin):
     model=User
     fields=["first_name","last_name","email","password","role"]
admin.site.register(User,AdminAuth)

