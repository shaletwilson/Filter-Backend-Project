from django.shortcuts import render
import pandas as pd
from pymongo import MongoClient
from django.shortcuts import render
from .models import flight_info
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import FlightSerializer, FlightDetailSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


def import_data(request):
    csv_file = "C:/Users/Shalet Wilson/Desktop/SearchApplication/filter_application/filter/Flugzeuginfo.xlsx"
    df = pd.read_excel(csv_file)

    # df.drop(columns=['id'], inplace=True)

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')

    # if 'id' in df.columns:
    #         # Drop the 'id' column from the DataFrame
    #         df.drop(columns=['id'], inplace=True)
    
    # Connect to MongoDB
    # client = MongoClient('localhost', 27017)
    # db = client['Flight_DataBase']
    # collection = db['filter_flight_info']
    

    # collection.insert_many(data)

    for item in data:
            flight_info.objects.create(
                icao_code=item['icao_code'], 
                manufacturer=item['manufacturer'], 
                type_model=item['type_model'],
                wake=item['wake'],
                crew_min=item['crew_min'],
                PAX_min=item['PAX_min'],
                PAX_max=item['PAX_max'],
                propulsion=item['propulsion'],
                engine_model=item['engine_model'],
                engine_power=item['engine_power'],

                speed=item['speed'],
                service_ceiling=item['service_ceiling'],
                range=item['range'],
                empty_weight=item['empty_weight'],
                Max_takeoff_weight=item['Max_takeoff_weight'],
                wing_span=item['wing_span'],
                wing_area=item['wing_area'],
                length=item['length'],
                height=item['height'],
                first_flight=item['first_flight'],

                production_status=item['production_status'],
                total_production=item['total_production'],
                data_for_version=item['data_for_version'],
                variants=item['variants'],
            )

    return render(request, 'import_success.html')



class Login(ObtainAuthToken):
      def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "user_id": user.id})
      



class FlightListCreateView(generics.ListCreateAPIView):
    queryset = flight_info.objects.all()
    serializer_class = FlightSerializer
    pagination_class = LargeResultsSetPagination


class FlightDetailView(RetrieveAPIView):
    queryset = flight_info.objects.all()
    serializer_class = FlightDetailSerializer
    lookup_field = 'id'



class Filter_API_View(APIView):
    pagination_class = LargeResultsSetPagination
    
    def post(self, request):
        data = request.data
        
        message = None
        filtered_data = None

        if not data:       
            filtered_data = flight_info.objects.all()
        else:
            column = data['column']  
            value = data['value']
            condition = data['condition']
            print("xxxxxxxxxxxxxxxxxxxx", column, value, condition)
            # column = 'manufacturer'
            # condition = 'startswith'
            # value = "air"
           
            if column and condition and value:
                if condition == '=':
                    if column == 'manufacturer':
                        filtered_data = flight_info.objects.filter(manufacturer__iexact=value)
                    elif column == 'icao_code':
                        filtered_data = flight_info.objects.filter(icao_code__iexact=value)
                    elif column == 'Max_takeoff_weight':
                        filtered_data = flight_info.objects.filter(Max_takeoff_weight=value)
                        print("TEST DATAAAAAA", filtered_data)
                    elif column == 'type_model':
                        filtered_data = flight_info.objects.filter(type_model__iexact=value)
                    else:
                        filtered_data = None
                        message = "NO Data"
                    
                elif condition == '<':
                    if column == 'Max_takeoff_weight':
                        filtered_data = flight_info.objects.filter(Max_takeoff_weight__lt=value)
                        print("data", filtered_data)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                elif condition == '>':
                    if column == 'Max_takeoff_weight':
                        filtered_data = flight_info.objects.filter(Max_takeoff_weight__gt=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                elif condition == '<=':
                    if column == 'Max_takeoff_weight':
                        filtered_data = flight_info.objects.filter(Max_takeoff_weight__lte=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                elif condition == '>=':
                    if column == 'Max_takeoff_weight':
                        filtered_data = flight_info.objects.filter(Max_takeoff_weight__gte=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                elif condition == 'contains':
                    print("yesssssssssss")
                    if column == 'manufacturer':
                        filtered_data = flight_info.objects.filter(manufacturer__icontains=value)
                        print("data", filtered_data)
                    elif column == 'icao_code':
                        filtered_data = flight_info.objects.filter(icao_code__icontains=value)
                    elif column == 'type_model':
                        filtered_data = flight_info.objects.filter(type_model__icontains=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                elif condition == 'startswith':
                    if column == 'manufacturer':
                        filtered_data = flight_info.objects.filter(manufacturer__istartswith=value)
                    elif column == 'icao_code':
                        filtered_data = flight_info.objects.filter(icao_code__istartswith=value)
                    elif column == 'type_model':
                        filtered_data = flight_info.objects.filter(type_model__istartswith=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"

            else:
                filtered_data = flight_info.objects.all()

            # Serialize data
        if filtered_data:
            serialized_data = FlightSerializer(filtered_data, many=True).data 
            response_data = {
                "response": serialized_data,
            }
        elif not filtered_data:
            response_data = {
                "response": "NO Data",
                "message": "Results Not Found"
            }
        else:
            response_data = {
                "response": "NO Data",
                "message": message
            }
        return Response(response_data)

