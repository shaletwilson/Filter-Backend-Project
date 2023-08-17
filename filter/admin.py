from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import flight_info

admin.site.register(flight_info)