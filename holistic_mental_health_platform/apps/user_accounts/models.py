from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class User(AbstractUser):
  objects = CustomUserManager()
  email = models.EmailField(unique=True, verbose_name='email')
  is_service_provider = models.BooleanField(default=False)
  is_client = models.BooleanField(default=False)
  #is_approved_blogger = models.BooleanField(default=False)
 
  


class ServiceProvider(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  
  phone_no = models.CharField(max_length=10, null=True)
  about = models.CharField(max_length=10000, null=True)
  # USERNAME_FIELD = 'email'
  # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  # def __str__(self):
  #     return "{}".format(self.email)


class Client(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  bio = models.CharField(max_length=1000, null=True)
  client_agree_to_T_and_Cs = models.BooleanField(default=False)

