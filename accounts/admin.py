from django.contrib import admin

# Register your models here.

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'bio', 'signup_confirmation']

admin.site.register(Profile, ProfileAdmin)