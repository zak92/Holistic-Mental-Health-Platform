from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import ClientUserCreationForm


# Register your models here.

class CustomUserAdmin(UserAdmin):
  model = User
  add_form = ClientUserCreationForm

  
  fieldsets = (
    *UserAdmin.fieldsets,
    (
      'User Role',
      {
        'fields': (
          'is_service_provider',
          'is_client' 
        )
      }
    )
  )


admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceProvider)
admin.site.register(Client)