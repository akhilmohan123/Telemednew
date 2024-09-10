from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,role,email,password):
        if not email:
            raise ValueError("User Must have an email")
        if not username:
            raise ValueError("User must have an username")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=role,
           
        )
        user.set_password(password=password)
       
        user.save(using=self._db)
        return user
    def create_superuser(self,first_name,last_name,email,username,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=3

        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
      Patient=1
      Doctor=2
      ADMIN=3
      ROLE_CHOICE=((Patient,"Patient"),(Doctor,"Doctor"),(ADMIN,"Admin"))
      role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
      first_name=models.CharField(max_length=25)
      last_name=models.CharField(max_length=25)
      password = models.CharField(max_length=128)
      username=models.CharField(max_length=25,unique=True)
      email=models.EmailField(max_length=100,unique=True)
      password = models.CharField(max_length=128)
      



      #required fields
      date_joined=models.DateTimeField(auto_now_add=True)
      last_login=models.DateTimeField(auto_now_add=True)
      created_date=models.DateTimeField(auto_now_add=True)
      is_admin=models.BooleanField(default=False)
      is_staff=models.BooleanField(default=False)
      is_active=models.BooleanField(default=False)
      is_superadmin=models.BooleanField(default=False)

      USERNAME_FIELD='email'
      REQUIRED_FIELDS=['username','first_name','last_name']
      objects=UserManager()
      def __str__(self):
          return self.email
      def has_perm(self,perm,obj=None):
          return self.is_admin
      def has_module_perms(self,app_label):
          return True

