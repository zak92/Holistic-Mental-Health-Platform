from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField

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
  is_approved_blogger = models.BooleanField(default=False)
  city = models.CharField(max_length=1024, null=True, blank=True)
  country = CountryField(blank_label='Select country', blank=True, null=True)
  profile_picture = models.ImageField(null=True, default='user.png')

  def __str__(self):
    return self.username
 

class ServiceProvider(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  about = RichTextField(blank=True, null=True)
  announcements = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.user.username



class Client(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  bio = models.CharField(max_length=1000, null=True, blank=True)
  status = models.TextField(null=True, blank=True)
  client_agree_to_T_and_Cs = models.BooleanField(default=False)
  
  def __str__(self):
    return self.user.username

