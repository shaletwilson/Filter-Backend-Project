from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import flight_info, Airport_Info, Airport_info_aip

admin.site.register(flight_info)
admin.site.register(Airport_info_aip)
