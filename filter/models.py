from django.db import models

# Create your models here.

from django.db import models

class flight_info(models.Model):
    icao_code = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=250, null=True, blank=True)
    type_model = models.CharField(max_length=250, null=True, blank=True)
    wake = models.CharField(max_length=50, null=True, blank=True)
    crew_min = models.CharField(max_length=50, null=True, blank=True)
    PAX_min = models.CharField(max_length=50, null=True, blank=True)
    PAX_max = models.CharField(max_length=50, null=True, blank=True)
    propulsion = models.CharField(max_length=250, null=True, blank=True)
    engine_model = models.CharField(max_length=250, null=True, blank=True)
    engine_power = models.CharField(max_length=250, null=True, blank=True)
    speed = models.CharField(max_length=250, null=True, blank=True)
    service_ceiling = models.CharField(max_length=250, null=True, blank=True)
    range = models.FloatField(null=True, blank=True)
    empty_weight = models.FloatField(null=True, blank=True)
    Max_takeoff_weight = models.FloatField(null=True, blank=True)
    wing_span = models.FloatField(null=True, blank=True)
    wing_area = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    first_flight = models.CharField(max_length=250, null=True, blank=True)
    production_status = models.CharField(max_length=250, null=True, blank=True)
    total_production = models.CharField(max_length=250, null=True, blank=True)
    data_for_version = models.CharField(max_length=250, null=True, blank=True)
    variants = models.CharField(max_length=250, null=True, blank=True)


    def __str__(self):
        return self.icao_code
