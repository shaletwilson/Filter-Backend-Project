from rest_framework import serializers
from .models import flight_info, Airport_Info, Airport_info_aip, Frequency, Runway, Image
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
        model = Airport_info_aip
        fields = ('id','name','country', 'geometry_coordinates', 'magneticDeclination', 'magneticDeclination', 'icaoCode')

class FrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequency
        fields = '__all__'

class RunwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Runway
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AirportInfoSerializer(serializers.ModelSerializer):
    frequency_set = FrequencySerializer(many=True, read_only=True)
    runway_set = RunwaySerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field, value in data.items(): 
            if isinstance(value, float) and math.isnan(value):
                data[field] = "No Data"
            elif isinstance(value, str) and value.lower() == "nan":
                data[field] = "No Data"

        return data
    class Meta:
        model = Airport_info_aip
        fields = '__all__'