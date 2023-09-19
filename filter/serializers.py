from rest_framework import serializers
from .models import flight_info, Airport_Info
import math

class FlightSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)

        for field, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[field] = "No Data"
            elif isinstance(value, str) and value.lower() == "nan":
                data[field] = "No Data"

        return data
    # def get_queryset(self):
    #     column = self.request.query_params.get('column')
    #     condition= self.request.query_params.get('condition')
    #     value = self.request.query_params.get('value')

        # queryset = flight_info.objects.filter(column=value)

    #     return queryset
    class Meta:
        model = flight_info
        fields = ('id','icao_code', 'manufacturer', 'Max_takeoff_weight', 'type_model')


class FlightDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        for field, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[field] = "No Data"
            elif isinstance(value, str) and value.lower() == "nan":
                data[field] = "No Data"

        return data
    class Meta:
        model = flight_info
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)

        for field, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[field] = "No Data"
            elif isinstance(value, str) and value.lower() == "nan":
                data[field] = "No Data"

        return data
    class Meta:
        model = Airport_Info
        fields = ('id','name', 'latitude_deg', 'longitude_deg', 'country_name', 'gps_code', 'iata_code')
