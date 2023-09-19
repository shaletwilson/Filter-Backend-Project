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



class Airport_Info(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    trafficType = models.CharField(max_length=255)
    magneticDeclination = models.FloatField()
    country = models.CharField(max_length=255)
    geometry = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    elevation = models.FloatField()
    value = models.FloatField()
    unit = models.CharField(max_length=255)
    referenceDatum = models.CharField(max_length=255)
    ppr = models.BooleanField()
    private = models.BooleanField()
    skydiveActivity = models.BooleanField()
    winchOnly = models.BooleanField()
    runways = models.IntegerField()
    designator = models.CharField(max_length=255)
    trueHeading = models.FloatField()
    alignedTrueNorth = models.FloatField()
    operations = models.CharField(max_length=255)
    mainRunway = models.CharField(max_length=255)
    turnDirection = models.CharField(max_length=255)
    takeOffOnly = models.BooleanField()
    landingOnly = models.BooleanField()
    surface = models.CharField(max_length=255)
    composition = models.CharField(max_length=255)
    mainComposite = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    mtow = models.FloatField()
    dimension = models.CharField(max_length=255)
    length = models.FloatField()
    width = models.FloatField()
    declaredDistance = models.FloatField()
    tora = models.FloatField()
    lda = models.FloatField()
    pilotCtrlLighting = models.CharField(max_length=255)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    createdBy = models.CharField(max_length=255)
    updatedBy = models.CharField(max_length=255)
    elevationGeoid = models.FloatField()
    geoidHeight = models.FloatField()
    hae = models.FloatField()

    def __str__(self):
        return self.name



class Airport_Info(models.Model):
    ident = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    latitude_deg = models.CharField(max_length=255, blank=True, null=True)
    longitude_deg = models.CharField(max_length=255, blank=True, null=True)
    elevation_ft = models.CharField(max_length=255, blank=True, null=True)
    continent = models.CharField(max_length=255, blank=True, null=True)
    country_name = models.CharField(max_length=255, blank=True, null=True)
    iso_country = models.CharField(max_length=255, blank=True, null=True)
    region_name = models.CharField(max_length=255, blank=True, null=True)
    iso_region = models.CharField(max_length=255, blank=True, null=True)
    local_region = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    scheduled_service = models.CharField(max_length=255, blank=True, null=True)
    gps_code = models.CharField(max_length=255, blank=True, null=True)
    iata_code = models.CharField(max_length=255, blank=True, null=True)
    home_link = models.URLField(max_length=255, blank=True, null=True)
    wikipedia_link = models.URLField(max_length=255, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
