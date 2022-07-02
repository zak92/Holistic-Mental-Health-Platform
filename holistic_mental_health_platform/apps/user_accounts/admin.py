from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import ClientUserCreationForm


# Register your models here.

class CustomUserAdmin(UserAdmin):
  model = User
  add_form = ClientUserCreationForm

  # To add your new fields to the detail view
  fieldsets = (
    *UserAdmin.fieldsets,
    (
      'Location', {
            'fields': (
                'city', 
                'country'
              )
        }
      ),
    (
      'User Role',
      {
        'fields': (
          'is_service_provider',
          'is_client' 
        )
      }
    ),
    (
      'Blog Writing Permission', {
            'fields': (
                'is_approved_blogger', 
              )
        }
    ),
    (
      'Profile Picture', {
            'fields': (
                'profile_picture', 
              )
        }
    ),
    
  )


admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceProvider)
admin.site.register(Client)