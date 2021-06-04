from django.contrib import admin

# Register your models here.

from .models import Profile, Seanses

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'signup_confirmation', 'status_of_user', 'data_of_registration', 'time_of_last_visit']

admin.site.register(Profile, ProfileAdmin)

class SeansesAdmin(admin.ModelAdmin):
    list_display = ['user', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read']

admin.site.register(Seanses, SeansesAdmin)