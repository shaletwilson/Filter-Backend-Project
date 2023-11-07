from django.shortcuts import render
import pandas as pd
from pymongo import MongoClient
from django.shortcuts import render
from .models import flight_info, Airport_Info
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import FlightSerializer, FlightDetailSerializer, AirportSerializer, AirportInfoSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListAPIView
import json
from django.db.models import Q
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


class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class Filter_API_View(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = FlightSerializer
    page_size = 100
    page = 1
    
    def get(self, request):  
        message = None
        filtered_data = None
        try:
            column = request.query_params.get('column')
            
            value = request.query_params.get('value')
            condition = request.query_params.get('condition')
        except:
            filtered_data = flight_info.objects.all().order_by('id')
       

        column = request.query_params.get('column')
        
        value = request.query_params.get('value')
        condition = request.query_params.get('condition')
                
        # column = 'manufacturer'
        # condition = 'startswith'
        # value = "air"
    
        if column and condition and value:
            if condition == '=':
                if column == 'manufacturer':
                    filtered_data = flight_info.objects.filter(manufacturer__iexact=value).order_by('id')
                elif column == 'icao_code':
                    filtered_data = flight_info.objects.filter(icao_code__iexact=value).order_by('id')
                elif column == 'Max_takeoff_weight':
                    filtered_data = flight_info.objects.filter(Max_takeoff_weight=value).order_by('id')
                    
                elif column == 'type_model':
                    filtered_data = flight_info.objects.filter(type_model__iexact=value).order_by('id')
                else:
                    filtered_data = None
                    message = "NO Data"
                
            elif condition == '<':
                if column == 'Max_takeoff_weight':
                    filtered_data = flight_info.objects.filter(Max_takeoff_weight__lt=value).order_by('id')
                
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == '>':
                if column == 'Max_takeoff_weight':
                    filtered_data = flight_info.objects.filter(Max_takeoff_weight__gt=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == '<=':
                if column == 'Max_takeoff_weight':
                    filtered_data = flight_info.objects.filter(Max_takeoff_weight__lte=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == '>=':
                if column == 'Max_takeoff_weight':
                    filtered_data = flight_info.objects.filter(Max_takeoff_weight__gte=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == 'contains':
                
                if column == 'manufacturer':
                    filtered_data = flight_info.objects.filter(manufacturer__icontains=value).order_by('id')
                    print("data", filtered_data)
                elif column == 'icao_code':
                    filtered_data = flight_info.objects.filter(icao_code__icontains=value).order_by('id')
                elif column == 'type_model':
                    filtered_data = flight_info.objects.filter(type_model__icontains=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == 'startswith':
                if column == 'manufacturer':
                    filtered_data = flight_info.objects.filter(manufacturer__istartswith=value).order_by('id')
                elif column == 'icao_code':
                    filtered_data = flight_info.objects.filter(icao_code__istartswith=value).order_by('id')
                elif column == 'type_model':
                    filtered_data = flight_info.objects.filter(type_model__istartswith=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            else:
                filtered_data = None
                message = "Select Proper Criteria For Filtering"

        else:
            filtered_data = flight_info.objects.all().order_by('id')

            # Serialize data
        if filtered_data:
            page = self.paginate_queryset(filtered_data)
            print("data", page)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                print("yes")
                print("serisl", serializer.data)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(filtered_data, many=True)
            response_data = {
                "response": serializer.data
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


    

class TestView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = FlightSerializer
    page_size = 100
    page = 1
    
    def get(self, request):
        message = None
        filtered_data = None
        try:
            filter_data = request.query_params.get('filters')
            filters = json.loads(filter_data)
            print("INITIAL DATA", filters)
            if not filters:
                filtered_data = flight_info.objects.all().order_by('id')

            for filter_item in filters:
                column = filter_item.get('column')
                condition = filter_item.get('condition')
                value = filter_item.get('value')

                if condition == '=':
                    if column == 'manufacturer':
                        filtered_data = filtered_data.filter(manufacturer__iexact=value) if filtered_data else flight_info.objects.filter(manufacturer__iexact=value)
                        print("xxxxxxxxxxxxxxxxxxxxxxxxxx", filtered_data)
                    elif column == 'icao_code':
                        filtered_data = filtered_data.filter(icao_code__iexact=value) if filtered_data else flight_info.objects.filter(icao_code__iexact=value)
                    elif column == 'Max_takeoff_weight':
                        
                        filtered_data = filtered_data.filter(Max_takeoff_weight=value) if filtered_data else flight_info.objects.filter(Max_takeoff_weight=value)
                        print("xxxxxxxxxxxxxxxxxxxxxxxxxx", filtered_data)
                    elif column == 'type_model':
                        filtered_data = filtered_data.filter(type_model__iexact=value) if filtered_data else flight_info.objects.filter(type_model__iexact=value)
                    else:
                        filtered_data = None
                        message = "NO Data"
                        break
                elif condition == '<':
                    if column == 'Max_takeoff_weight':
                        filtered_data = filtered_data.filter(Max_takeoff_weight__lt=value) if filtered_data else flight_info.objects.filter(Max_takeoff_weight__lt=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                        break
                elif condition == '>':
                    if column == 'Max_takeoff_weight':
                        print("PREVIOUS DATA", filtered_data)
                        filtered_data = filtered_data.filter(Max_takeoff_weight__gt=value) if filtered_data else flight_info.objects.filter(Max_takeoff_weight__gt=value)
                        print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY", filtered_data)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                        break
                elif condition == '<=':
                    if column == 'Max_takeoff_weight':
                        filtered_data = filtered_data.filter(Max_takeoff_weight__lte=value) if filtered_data else flight_info.objects.filter(Max_takeoff_weight__lte=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                        break
                elif condition == '>=':
                    if column == 'Max_takeoff_weight':
                        filtered_data = filtered_data.filter(Max_takeoff_weight__gte=value) if filtered_data else flight_info.objects.filter(Max_takeoff_weight__gte=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                        break
                elif condition == 'contains':
                    if column == 'manufacturer':
                        filtered_data = filtered_data.filter(manufacturer__icontains=value) if filtered_data else flight_info.objects.filter(manufacturer__icontains=value)
                    elif column == 'icao_code':
                        filtered_data = filtered_data.filter(type_modicao_code__icontainsel__iexact=value) if filtered_data else flight_info.objects.filter(icao_code__icontains=value)
                    elif column == 'type_model':
                        filtered_data = filtered_data.filter(type_model__icontains=value) if filtered_data else flight_info.objects.filter(type_model__icontains=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                        break
                elif condition == 'startswith':
                    if column == 'manufacturer':
                        filtered_data = filtered_data.filter(manufacturer__istartswith=value) if filtered_data else flight_info.objects.filter(manufacturer__istartswith=value)
                    elif column == 'icao_code':
                        filtered_data = filtered_data.filter(icao_code__istartswith=value) if filtered_data else flight_info.objects.filter(icao_code__istartswith=value)
                    elif column == 'type_model':
                        filtered_data = filtered_data.filter(type_model__istartswith=value) if filtered_data else flight_info.objects.filter(type_model__istartswith=value)
                    else:
                        filtered_data = None
                        message = "Select Proper Criteria For Filtering"
                        break
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
                    break
            
            if filtered_data:
                
                page = self.paginate_queryset(filtered_data)
                
                if page is not None:
                   
                    serializer = self.get_serializer(page, many=True)
                    

                    return self.get_paginated_response(serializer.data)
                
                serializer = self.get_serializer(filtered_data, many=True)
                
                response_data = {
                    "response": serializer.data
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
            

        except Exception as e:
            print("exception", e)
            response_data = {
                "response": "Error",
                "message": str(e)
            }
        print("respones", response_data)
        return Response(response_data)


def import_airport_data(request):
    excel_file = "C:/Users/Shalet Wilson/Desktop/SearchApplication/filter_application/filter/de-airports.xlsx"
    df = pd.read_excel(excel_file)

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
            Airport_Info.objects.create(
                ident=item['ident'], 
                type=item['type'], 
                name=item['name'],
                latitude_deg=item['latitude_deg'],
                longitude_deg=item['longitude_deg'],
                elevation_ft=item['elevation_ft'],
                continent=item['continent'],
                country_name=item['country_name'],
                iso_country=item['iso_country'],
                iso_region=item['iso_region'],

                region_name=item['region_name'],
                local_region=item['local_region'],
                municipality=item['municipality'],
                scheduled_service=item['scheduled_service'],
                gps_code=item['gps_code'],
                iata_code=item['iata_code'],
                home_link=item['home_link'],
                wikipedia_link=item['wikipedia_link'],
                keywords=item['keywords'],
                score=item['score'],

                last_updated=item['last_updated'],
                
            )

    return render(request, 'import_success.html')



# def import_airport_data_all(request):
#     excel_file = "C:/Users/Shalet Wilson/Desktop/SearchApplication/filter_application/filter/de-airports.xlsx"
#     df = pd.read_excel(excel_file)

#     # df.drop(columns=['id'], inplace=True)

#     # Convert the DataFrame to a list of dictionaries
#     data = df.to_dict(orient='records')

#     # if 'id' in df.columns:
#     #         # Drop the 'id' column from the DataFrame
#     #         df.drop(columns=['id'], inplace=True)
    
#     # Connect to MongoDB
#     # client = MongoClient('localhost', 27017)
#     # db = client['Flight_DataBase']
#     # collection = db['filter_flight_info']
    

#     # collection.insert_many(data)

#     for item in data:
#             if not item[source] ='AIP':
           
#                 Airport_Info.objects.create(
#                     ident=item['ident'], 
#                     type=item['type'], 
#                     name=item['name'],
#                     latitude_deg=item['latitude_deg'],
#                     longitude_deg=item['longitude_deg'],
#                     elevation_ft=item['elevation_ft'],
#                     continent=item['continent'],
#                     country_name=item['country_name'],
#                     iso_country=item['iso_country'],
#                     iso_region=item['iso_region'],

#                     region_name=item['region_name'],
#                     local_region=item['local_region'],
#                     municipality=item['municipality'],
#                     scheduled_service=item['scheduled_service'],
#                     gps_code=item['gps_code'],
#                     iata_code=item['iata_code'],
#                     home_link=item['home_link'],
#                     wikipedia_link=item['wikipedia_link'],
#                     keywords=item['keywords'],
#                     score=item['score'],

#                     last_updated=item['last_updated'],
                    
#                 )
#             else:
#                 Airport_Info.objects.create(
                    
#                     name=item['name'], 
#                     type=item['type'], 
#                     traffic_type=item['traffic_type'],
                    
#                     country=item['country'], 
#                     magnetic_declination=item['magnetic_declination'],

#                     geometry=item['geometry'], 
#                         type=item['type'], 
#                         coordinates=item['coordinates'],

#                     elevation=item['elevation'], 
#                         value=item['value'], 
#                         unit=item['unit'],
#                         referenceDatum=item['referenceDatum'], 

#                     ppr=item['ppr'], 
#                     private=item['private'],
#                     skydiveActivity=item['skydiveActivity'], 
#                     winchOnly=item['winchOnly'], 
                    
#                     createdAt=item['createdAt'],
#                     updatedAt=item['updatedAt'], 
#                     createdBy=item['createdBy'],
#                     updatedBy=item['updatedBy'], 
#                     elevationGeoid=item['elevationGeoid'], 
#                         geoidHeight=item['geoidHeight'], 
#                         hae=item['hae'],
#                 )
                    

#     return render(request, 'import_success.html')



class AirportListView(generics.ListCreateAPIView):
    queryset = Airport_Info.objects.all()
    serializer_class = AirportSerializer
    # pagination_class = LargeResultsSetPagination


class AirportDetailView(RetrieveAPIView):
    queryset = Airport_Info.objects.all()
    print("data", queryset)
    serializer_class = AirportInfoSerializer
    lookup_field = 'id'




class Airport_Filter_API(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = AirportSerializer
    page_size = 100
    page = 1
    
    def get(self, request):  
        message = None
        filtered_data = None
        try:
            filed_name = request.query_params.get('field_name')
            
            value = request.query_params.get('value')
            condition = request.query_params.get('condition')
        except:
            filtered_data = Airport_Info.objects.all().order_by('id')
       

        filed_name = request.query_params.get('filed_name')
        
        value = request.query_params.get('value')
        condition = request.query_params.get('condition')

        if filed_name and condition and value:
            if condition == '=':
                if filed_name == 'name':
                    filtered_data = Airport_Info.objects.filter(name__iexact=value).order_by('id')
                elif filed_name == 'iata_code':
                    filtered_data = Airport_Info.objects.filter(iata_code__iexact=value).order_by('id')
                elif filed_name == 'Max_takeoff_weight':
                    filtered_data = Airport_Info.objects.filter(Max_takeoff_weight=value).order_by('id')
                else:
                    filtered_data = None
                    message = "NO Data"
                
            elif condition == '<':
                if filed_name == 'Max_takeoff_weight':
                    filtered_data = Airport_Info.objects.filter(Max_takeoff_weight__lt=value).order_by('id')
                
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == '>':
                if filed_name == 'Max_takeoff_weight':
                    filtered_data = Airport_Info.objects.filter(Max_takeoff_weight__gt=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == '<=':
                if filed_name == 'Max_takeoff_weight':
                    filtered_data = Airport_Info.objects.filter(Max_takeoff_weight__lte=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == '>=':
                if filed_name == 'Max_takeoff_weight':
                    filtered_data = Airport_Info.objects.filter(Max_takeoff_weight__gte=value).order_by('id')
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == 'contains':
                
                if filed_name == 'name':
                    filtered_data = Airport_Info.objects.filter(name__icontains=value).order_by('id')
                    print("data", filtered_data)
                elif filed_name == 'iata_code':
                    filtered_data = Airport_Info.objects.filter(iata_code__icontains=value).order_by('id')
                
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            elif condition == 'startswith':
                if filed_name == 'name':
                    filtered_data = Airport_Info.objects.filter(name__istartswith=value).order_by('id')
                elif filed_name == 'iata_code':
                    filtered_data = Airport_Info.objects.filter(iata_code__istartswith=value).order_by('id')
                
                else:
                    filtered_data = None
                    message = "Select Proper Criteria For Filtering"
            else:
                filtered_data = None
                message = "Select Proper Criteria For Filtering"

        else:
            filtered_data = Airport_Info.objects.all().order_by('id')

            # Serialize data
        if filtered_data:
            page = self.paginate_queryset(filtered_data)
            print("data", page)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                print("yes")
                print("serisl", serializer.data)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(filtered_data, many=True)
            response_data = {
                "response": serializer.data
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


