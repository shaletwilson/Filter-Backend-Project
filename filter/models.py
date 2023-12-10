from djongo import models

# Create your models here.

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
    max_speed = models.CharField(max_length=250, null=True, blank=True)
    payload = models.CharField(max_length=250, null=True, blank=True)
    noise = models.CharField(max_length=250, null=True, blank=True)
    project_started_year = models.CharField(max_length=250, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)

def __str__(self):
    return self.icao_code

# DB Design from Chat GPT for AIP Data
# Starting
class Airport_info_aip(models.Model):
    name = models.CharField(max_length=255)
    icaoCode = models.CharField(max_length=15, blank=True, null=True)
    airport_type = models.CharField(max_length=250, blank=True, null=True)
    trafficType = models.JSONField(blank=True, null=True)
    magneticDeclination = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    geometry_type = models.CharField(max_length=255, blank=True, null=True)
    geometry_coordinates = models.JSONField(blank=True, null=True)
    elevation_value = models.CharField(max_length=250, blank=True, null=True)
    elevation_unit = models.CharField(max_length=250, blank=True, null=True)
    elevation_referenceDatum = models.CharField(max_length=250, blank=True, null=True)
    ppr = models.CharField(max_length=250, blank=True, null=True)
    private = models.CharField(max_length=250, blank=True, null=True)
    skydiveActivity = models.CharField(max_length=250, blank=True, null=True)
    winchOnly = models.CharField(max_length=250, blank=True, null=True)
    elevation_geoid_height = models.CharField(max_length=250, blank=True, null=True)
    elevation_hae = models.CharField(max_length=250, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    services_fuelTypes = models.JSONField(blank=True, null=True)
    services_gliderTowing = models.JSONField(blank=True, null=True)
    created_at = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    ident = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
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
    Max_takeoff_weight = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Frequency(models.Model):
    airport = models.ForeignKey(Airport_info_aip, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, blank=True, null=True)
    unit = models.CharField(max_length=250, blank=True, null=True)
    frequency_type = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    primary = models.CharField(max_length=255, blank=True, null=True)
    publicUse = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.value} - {self.name} ({'Primary' if self.primary else 'Secondary'})"


class Runway(models.Model):
    airport = models.ForeignKey(Airport_info_aip, on_delete=models.CASCADE)
    designator = models.CharField(max_length=10, blank=True, null=True)
    trueHeading = models.CharField(max_length=250, blank=True, null=True)
    alignedTrueNorth = models.CharField(max_length=250, blank=True, null=True)
    operations = models.CharField(max_length=250, blank=True, null=True)
    mainRunway = models.CharField(max_length=250, blank=True, null=True)
    turnDirection = models.CharField(max_length=250, blank=True, null=True)
    takeOffOnly = models.CharField(max_length=250, blank=True, null=True)
    landingOnly = models.CharField(max_length=250, blank=True, null=True)
    surface_composition = models.JSONField(blank=True, null=True)
    surface_mainComposite = models.CharField(max_length=250, blank=True, null=True)
    surface_condition = models.CharField(max_length=250, blank=True, null=True)
    surface_mtow_value = models.CharField(max_length=250, blank=True, null=True)
    surface_mtow_unit = models.CharField(max_length=250, blank=True, null=True)
    dimension_length_value = models.CharField(max_length=250, blank=True, null=True)
    dimension_length_unit = models.CharField(max_length=250, blank=True, null=True)
    dimension_width_value = models.CharField(max_length=250, blank=True, null=True)
    dimension_width_unit = models.CharField(max_length=250, blank=True, null=True)
    declaredDistance_tora_value = models.CharField(max_length=250, blank=True, null=True)
    declaredDistance_tora_unit = models.CharField(max_length=250, blank=True, null=True)
    declaredDistance_lda_value = models.CharField(max_length=250, blank=True, null=True)
    declaredDistance_lda_unit = models.CharField(max_length=250, blank=True, null=True)
    pilotCtrlLighting = models.CharField(max_length=250, blank=True, null=True)
    visualApproachAids = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.designator} - {self.airport.name} Runway"


class Image(models.Model):
    airport = models.ForeignKey(Airport_info_aip, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.filename


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
    Max_takeoff_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name




