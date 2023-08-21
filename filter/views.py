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
from rest_framework.generics import ListAPIView

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
    page_size = 100  # Set your desired page size here
    page_size_query_param = 'page_size'
    max_page_size = 1000


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




class TestView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = FlightSerializer
    page_size = 2
    page = 1
    
    def get(self, request):       
        column = request.query_params.get('column')
        print("column", column)
        value = request.query_params.get('value')
        condition = request.query_params.get('condition')

        if column == 'manufacturer':
            filtered_data = flight_info.objects.filter(manufacturer__icontains=value)
        
        # paginated_data = self.pagination_class().paginate_queryset(filtered_data, request)
        
        
        # serialized_data = FlightSerializer(paginated_data, many=True).data
        # print("serialised data", paginated_data)
        
        page = self.paginate_queryset(filtered_data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_data, many=True)
        return Response(serializer.data)
        



        # response_data = {
        #     "response": serialized_data,
        # }
        # # return self.pagination_class().get_paginated_response(response_data)
        # return self.pagination_class().get_paginated_response(response_data)
