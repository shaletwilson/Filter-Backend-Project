from django.shortcuts import render
import pandas as pd
from pymongo import MongoClient
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Airport_info_aip,  Frequency, Runway, Image, flight_info, Airport_Info
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

@csrf_exempt
def import_aircraft_data(request):
    if request.method == 'POST':
        
        uploaded_file = request.FILES.get('file')
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        data = df.to_dict(orient='records')


        for item in data:
                flight_info.objects.create(
                    icao_code=item['icao_code'] if 'icaoCode' in item else "", 
                    manufacturer=item['manufacturer'] if 'manufacturer' in item else "", 
                    type_model=item['type_model'] if 'type_model' in item else "",
                    wake=item['wake'] if 'wake' in item else "",
                    crew_min=item['crew_min'] if 'crew_min' in item else "",
                    PAX_min=item['PAX_min'] if 'PAX_min' in item else "",
                    PAX_max=item['PAX_max'] if 'PAX_max' in item else "",
                    propulsion=item['propulsion'] if 'propulsion' in item else "",
                    engine_model=item['engine_model'] if 'engine_model' in item else "",
                    engine_power=item['engine_power'] if 'engine_power' in item else "",

                    speed=item['speed'] if 'speed' in item else "",
                    service_ceiling=item['service_ceiling'] if 'service_ceiling' in item else "",
                    range=item['range'] if 'range' in item else 0,
                    empty_weight=item['empty_weight'] if 'empty_weight' in item else 0,
                    Max_takeoff_weight=item['Max_takeoff_weight'] if 'Max_takeoff_weight' in item else 0,
                    wing_span=item['wing_span'] if 'wing_span' in item else 0,
                    wing_area=item['wing_area'] if 'wing_area' in item else 0,
                    length=item['length'] if 'length' in item else 0,
                    height=item['height'] if 'height' in item else 0,
                    first_flight=item['first_flight'] if 'first_flight' in item else "",

                    production_status=item['production_status'] if 'production_status' in item else "",
                    total_production=item['total_production'] if 'total_production' in item else "",
                    data_for_version=item['data_for_version'] if 'data_for_version' in item else "",
                    variants=item['variants'] if 'variants' in item else "",
                    max_speed=item['max_speed'] if 'max_speed' in item else "",
                    payload=item['payload'] if 'payload' in item else "",
                    noise=item['noise'] if 'noise' in item else "",
                    project_started_year=item['project_started_year'] if 'project_started_year' in item else "",
                    category=item['category'] if 'category' in item else "",
                )

        return JsonResponse({'message': 'Import successfull'}, status=200 )
    else:
        return JsonResponse({'error': 'File not provided'}, status=400)



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
    page_size = 1500
    page_size_query_param = 'page_size'
    max_page_size = 1500


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
                    filtered_data = flight_info.objects.all().order_by('id')
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


def import_airport_data_aip(request):
    if request.method == 'POST':
        selected_source = request.POST.get('selectedSource', '')
        
        uploaded_file = request.FILES.get('file')
        

        if selected_source == "Other Source":
            df = pd.read_excel(uploaded_file)

            data = df.to_dict(orient='records')
            for item in data:
                
            
                Airport_info_aip.objects.get_or_create(
                    ident=item['ident'] if 'ident' in item else "", 
                    type=item['type'] if 'type' in item else "", 
                    name=item['name'] if 'name' in item else "",
                    latitude_deg=item['latitude_deg'] if 'latitude_deg' in item else "",
                    longitude_deg=item['longitude_deg'] if 'longitude_deg' in item else "",
                    elevation_ft=item['elevation_ft'] if 'elevation_ft' in item else "",
                    continent=item['continent'] if 'continent' in item else "",
                    country_name=item['country_name'] if 'country_name' in item else "",
                    iso_country=item['iso_country'] if 'iso_country' in item else "",
                    iso_region=item['iso_region'] if 'iso_region' in item else "",
                    region_name=item['region_name'] if 'region_name' in item else "",
                    local_region=item['local_region'] if 'local_region' in item else "",
                    municipality=item['municipality'] if 'municipality' in item else "",
                    scheduled_service=item['scheduled_service'] if 'scheduled_service' in item else "",
                    gps_code=item['gps_code'] if 'gps_code' in item else "",
                    iata_code=item['iata_code'] if 'iata_code' in item else "",
                    home_link=item['home_link'] if 'home_link' in item else "",
                    wikipedia_link=item['wikipedia_link'] if 'wikipedia_link' in item else "",
                    keywords=item['keywords'] if 'keywords' in item else "",
                    score=item['score'] if 'score' in item else "",
                    last_updated=item['last_updated'] if 'last_updated' in item else "",
                    Max_takeoff_weight=item['Max_takeoff_weight'] if 'Max_takeoff_weight' in item else "",
                    
                )
        
        else:

            uploaded_file = request.FILES.get('file')

            with open(uploaded_file, 'r') as file:
                    json_data = json.load(file)

            for item in json_data:
                    
                    airport_new=Airport_info_aip(
                        name=item['name'] if 'name' in item else "",
                        icaoCode=item['icaoCode'] if 'icaoCode' in item else "",
                        airport_type=item['type'] if 'type' in item else "", 
                        trafficType=list([(item['trafficType'])]) if 'trafficType' in item else list([("")]),
                        magneticDeclination=item['magneticDeclination'] if 'magneticDeclination' in item else "",
                        country=item['country'] if 'country' in item else "",
                        geometry_type=item['geometry']['type'] if 'geometry' in item and 'type' in item['geometry'] else "",
                        geometry_coordinates=list([(item['geometry']['coordinates'])]) if 'geometry' in item and 'coordinates' in item['geometry'] else list([("")]),
                        elevation_value=item['elevation']['value'] if 'elevation' in item and 'value' in item['elevation'] else "",
                        elevation_unit=item['elevation']['unit'] if 'elevation' in item and 'unit' in item['elevation'] else "",
                        elevation_referenceDatum=item['elevation']['referenceDatum'] if 'elevation' in item and 'referenceDatum' in item['elevation'] else "",
                        ppr=item['ppr'] if 'ppr' in item else "",
                        private=item['private'] if 'private' in item else "",
                        skydiveActivity=item['skydiveActivity'] if 'skydiveActivity' in item else "",
                        winchOnly=item['winchOnly'] if 'winchOnly' in item else "",
                        elevation_geoid_height=item['elevationGeoid']['geoidHeight'] if 'elevationGeoid' in item and 'geoidHeight' in item['elevationGeoid'] else "",
                        elevation_hae=item['elevationGeoid']['hae'] if 'elevationGeoid' in item and 'hae' in item['elevationGeoid'] else "",
                        contact=item['contact'] if 'contact' in item else "",
                        services_fuelTypes=list([(item['services']['fuelTypes'])]) if 'services' in item and 'fuelTypes' in item['services'] else list([("")]),
                        services_gliderTowing=list([(item['services']['gliderTowing'])]) if 'services' in item and 'gliderTowing' in item['services'] else list([("")]),
                        created_at=item['createdAt'] if 'createdAt' in item else "",
                        created_by=item['createdBy'] if 'createdBy' in item else "",
                        updated_at=item['updatedAt'] if 'updatedAt' in item else "",
                        updated_by=item['updatedBy'] if 'updatedBy' in item else "",
                    )
                    airport_new.save()

                    if 'frequencies' in item:
                        for frequency in item['frequencies']:
                            frequency_new=Frequency(
                                airport=airport_new,
                                value=frequency['value'] if 'frequencies' in item and 'value' in frequency else "",
                                unit=frequency['unit'] if 'frequencies' in item and 'unit' in frequency else "",
                                frequency_type=frequency['type'] if 'frequencies' in item and 'type' in frequency else "",
                                name=frequency['name'] if 'frequencies' in item and 'name' in frequency else "",
                                primary=frequency['primary'] if 'frequencies' in item and 'primary' in frequency else "",
                                publicUse=frequency['publicUse'] if 'frequencies' in item and 'publicUse' in frequency else "",
                            )
                            
                            frequency_new.save()
                    
                    if 'runways' in item:
                        for runway in item['runways']:
                            runway_new=Runway(
                                airport = airport_new,
                                designator = runway['designator'] if 'runways' in item and 'designator' in runway else "",
                                trueHeading = runway['trueHeading'] if 'runways' in item and 'trueHeading' in runway else "",
                                alignedTrueNorth = runway['alignedTrueNorth'] if 'runways' in item and 'alignedTrueNorth' in runway else "",
                                operations = runway['operations'] if 'runways' in item and 'operations' in runway else "",
                                mainRunway = runway['mainRunway'] if 'runways' in item and 'mainRunway' in runway else "",
                                turnDirection = runway['turnDirection'] if 'runways' in item and 'turnDirection' in runway else "",
                                takeOffOnly = runway['takeOffOnly'] if 'runways' in item and 'takeOffOnly' in runway else "",
                                landingOnly = runway['landingOnly'] if 'runways' in item and 'landingOnly' in runway else "",
                                surface_composition = list([(runway['surface']['composition'])]) if 'runways' in item and 'surface' in runway and 'composition' in runway['surface'] else list([("")]),
                                surface_mainComposite = runway['surface']['mainComposite'] if 'runways' in item and 'surface' in runway and 'mainComposite' in runway['surface'] else "",
                                surface_condition = runway['surface']['condition'] if 'runways' in item and 'surface' in runway and 'condition' in runway['surface'] else "",
                                surface_mtow_value = runway['surface']['mtow']['value'] if 'runways' in item and 'surface' in runway and 'mtow' in runway['surface'] and 'value' in runway['surface']['mtow'] else "",
                                surface_mtow_unit = runway['surface']['mtow']['unit'] if 'runways' in item and 'surface' in runway and 'mtow' in runway['surface'] and 'unit' in runway['surface']['mtow'] else "",
                                # dimension_length_value = runway['length']['value'] if 'runways' in item and 'length' in runway and 'value' in runway['length'] else "",
                                dimension_length_value = (runway['dimension']['length']['value'] if 'dimension' in runway and 'length' in runway['dimension'] and 'value' in runway['dimension']['length'] else ""),

                                #dimension_length_unit = runway['length']['unit'] if 'runways' in item and 'length' in runway and 'unit' in runway['length'] else "",
                                dimension_length_unit = (runway['dimension']['length']['unit'] if 'dimension' in runway and 'length' in runway['dimension'] and 'unit' in runway['dimension']['length'] else ""),
                                # dimension_width_value = runway['width']['value'] if 'runways' in item and 'width' in runway and 'value' in runway['width'] else "",
                                # dimension_width_unit = runway['width']['unit'] if 'runways' in item and 'width' in runway and 'unit' in runway['width']  else "",
                                dimension_width_value = (runway['dimension']['width']['value'] if 'dimension' in runway and 'width' in runway['dimension'] and 'value' in runway['dimension']['width'] else ""),
                                dimension_width_unit = (runway['dimension']['width']['unit'] if 'dimension' in runway and 'width' in runway['dimension'] and 'unit' in runway['dimension']['width'] else ""),
                                declaredDistance_tora_value = runway['declaredDistance']['tora']['value'] if 'runways' in item and 'declaredDistance' in runway and 'tora' in runway['declaredDistance'] and 'value' in runway['declaredDistance']['tora'] else "",
                                declaredDistance_tora_unit = runway['declaredDistance']['tora']['unit'] if 'runways' in item and 'declaredDistance' in runway and 'tora' in runway['declaredDistance'] and 'unit' in runway['declaredDistance']['tora'] else "",
                                declaredDistance_lda_value = runway['declaredDistance']['lda']['value'] if 'runways' in item and 'declaredDistance' in runway and 'lda' in runway['declaredDistance'] and 'value' in runway['declaredDistance']['lda'] else "",
                                declaredDistance_lda_unit = runway['declaredDistance']['lda']['unit'] if 'runways' in item and 'declaredDistance' in runway and 'lda' in runway['declaredDistance'] and 'unit' in runway['declaredDistance']['lda'] else "",
                                pilotCtrlLighting = runway['pilotCtrlLighting'] if 'runways' in item and 'pilotCtrlLighting' in runway else "",
                                visualApproachAids = list([(runway['visualApproachAids'])]) if 'runways' in item and 'visualApproachAids' in runway else list([("")]),
                            )
                            runway_new.save()
                    
                    if 'images' in item:
                        for image in item["images"]:
                            image_new=Image(
                                airport = airport_new,
                                filename=image['filename'] if 'images' in item and 'filename' in image else ""
                            )
                            image_new.save()
            return JsonResponse({'message': 'Import successfull'}, status=200 )
    else:
        return JsonResponse({'error': 'File not provided'}, status=400)
    



# def import_airport_data_all(request):
#     excel_file = "C:/Users/Shalet Wilson/Desktop/SearchApplication/filter_application/filter/de-airports.xlsx"
#     df = pd.read_excel(excel_file)
        
    #   data = df.to_dict(orient='records')
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
    queryset = Airport_info_aip.objects.all()
    serializer_class = AirportSerializer
    # pagination_class = LargeResultsSetPagination


class AirportDetailView(RetrieveAPIView):
    queryset = Airport_info_aip.objects.all()
    serializer_class = AirportInfoSerializer
    lookup_field = 'id'

    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()

    #     # Fetch related Frequency data for the airport
    #     frequencies = Frequency.objects.filter(airport=instance)

    #     # Pass the fetched Frequency data to the serializer
    #     serializer = self.get_serializer(instance, frequencies=frequencies)

    #     return Response(serializer.data)
    # def get_object(self):
    #     # Override the get_object method to prefetch_related runways, frequencies, and images
    #     obj = super().get_object()
    #     return Airport_info_aip.objects.prefetch_related('runways').get(pk=obj.pk)




class Airport_Filter_API(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = AirportSerializer
    page_size = 1000
    page = 1
    
    def get_queryset(self):    
        message = None
        filtered_data = None
        try:
            filed_name = self.request.query_params.get('column')
            print("data from call", filed_name)
            
            value = self.request.query_params.get('value')
            condition = self.request.query_params.get('condition')
        except:
            filtered_data = Airport_info_aip.objects.all().order_by('id')
       

        filed_name = self.request.query_params.get('column')
        
        value = self.request.query_params.get('value')
        condition = self.request.query_params.get('condition')
        # filed_name = 'MTOW'
        # value = '4'
        # condition = '<='

        if filed_name and condition and value:
            print("Trueeeee", condition)
            if condition == '=':
                print("data ======")
                if filed_name == 'name':
                    filtered_data = Airport_info_aip.objects.filter(name__iexact=value).order_by('id')
                    
                elif filed_name == 'icaoCode':
                    filtered_data = Airport_info_aip.objects.filter(icaoCode__iexact=value).order_by('id')
                elif filed_name == 'MTOW':
                    filtered_data = Airport_info_aip.objects.filter(runway__surface_mtow_value=value).order_by('id')
                    print("data from aip", filtered_data)

                else:
                    filtered_data = None
                    self.message = "NO Data"
                
            elif condition == '<':
                if filed_name == 'MTOW':
                    filtered_data = Airport_info_aip.objects.filter(runway__surface_mtow_value__lt=value).order_by('id')
                
                else:
                    filtered_data = None
                    self.message = "Select Proper Criteria For Filtering"
            elif condition == '>':
                if filed_name == 'MTOW':
                    filtered_data = Airport_info_aip.objects.filter(runway__surface_mtow_value__gt=value).order_by('id')
                else:
                    filtered_data = None
                    self.message = "Select Proper Criteria For Filtering"
            elif condition == '<=':
                if filed_name == 'MTOW':
                    filtered_data = Airport_info_aip.objects.filter(runway__surface_mtow_value__lte=value).order_by('id')
                else:
                    filtered_data = None
                    self.message = "Select Proper Criteria For Filtering"
            elif condition == '>=':
                if filed_name == 'MTOW':
                    filtered_data = Airport_info_aip.objects.filter(runway__surface_mtow_value__gte=value).order_by('id')
                else:
                    filtered_data = None
                    self.message = "Select Proper Criteria For Filtering"
            elif condition == 'contains':
                
                if filed_name == 'name':
                    filtered_data = Airport_info_aip.objects.filter(name__icontains=value).order_by('id')
                    print("data", filtered_data)
                elif filed_name == 'icaoCode':
                    filtered_data = Airport_info_aip.objects.filter(icaoCode__icontains=value).order_by('id')
                    print("contains", filtered_data)
                
                else:
                    filtered_data = None
                    self.message = "Select Proper Criteria For Filtering"
            elif condition == 'startswith':
                if filed_name == 'name':
                    filtered_data = Airport_info_aip.objects.filter(name__istartswith=value).order_by('id')
                elif filed_name == 'icaoCode':
                    filtered_data = Airport_info_aip.objects.filter(icaoCode__istartswith=value).order_by('id')
                
                else:
                    filtered_data = None
                    self.message = "Select Proper Criteria For Filtering"
            else:
                filtered_data = None
                self.message = "Select Proper Criteria For Filtering"

        else:
            filtered_data = Airport_info_aip.objects.all().order_by('id')

        return filtered_data
    
    # Serialize data
    def list(self, request, *args, **kwargs):
        # message = self.message
        # if not message:
        #     message = "No Data"
        queryset = self.get_queryset()

        if queryset:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            response_data = {"response": serializer.data}
        else:
            response_data = {"response": "NO Data", "message": getattr(self, 'message', "Results Not Found")}

        return Response(response_data)
        # if filtered_data:
                
        #         page = self.paginate_queryset(filtered_data)
                
        #         if page is not None:
                   
        #             serializer = self.get_serializer(page, many=True)
                    

        #             return self.get_paginated_response(serializer.data)
                
        #         serializer = self.get_serializer(filtered_data, many=True)
                
        #         response_data = {
        #             "response": serializer.data
        #         }
        # elif not filtered_data:
        #     response_data = {
        #         "response": "NO Data",
        #         "message": "Results Not Found"
        #     }
        # else:
        #     response_data = {
        #         "response": "NO Data",
        #         "message": message
        #     }
        # return Response(response_data)


def truncate_float(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier


def are_coordinates_close(geocoords_lat, geocoords_long, lat_deg,long_deg, tolerance=0.005):
    """
    Check if two sets of coordinates are close within a specified tolerance.
    Default tolerance is 0.005 degrees.(500m)
    """
    print("DATA FROM COORDINATES TOLERANCE", abs(geocoords_lat - lat_deg) < tolerance or abs(geocoords_long - long_deg) < tolerance)
    return abs(geocoords_lat - lat_deg) < tolerance or abs(geocoords_long - long_deg) < tolerance

# Example usage



def import_airport_data_othersource(file_path):
    # airport_coords = (50.0386, 8.559)
    # other_coords = (50.0365, 8.561)

    # if are_coordinates_close(airport_coords[0], airport_coords[1], other_coords[0], other_coords[1]):
    #     print("Coordinates are close.")
    # else:
    #     print("Coordinates are not close.")
    excel_file = "C:/Users/Shalet Wilson/Desktop/SearchApplication/filter_application/filter/de-airports.xlsx"
    df = pd.read_excel(excel_file)
        
    data = df.to_dict(orient='records')
    found_count = 0
    not_found_count = 0
    total_record = 0
    for item in data:
        latitude_deg=item['latitude_deg']
        
        lat_deg = truncate_float(latitude_deg,3)
        
        longitude_deg=item['longitude_deg'] 
        long_deg = truncate_float(longitude_deg,3)
        
        airports = Airport_info_aip.objects.all()
    # for index, row in excel_data.iterrows():
        for airport in airports:
            print(airport.geometry_coordinates[0])
            geocoords_long = truncate_float(airport.geometry_coordinates[0][0],3)
            geocoords_lat = truncate_float(airport.geometry_coordinates[0][1],3)
            print(geocoords_long, geocoords_lat)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("lat from excel", lat_deg)
            print("long from excel", long_deg)
            print("lat from model", geocoords_lat)
            print("long from model", geocoords_long)
            total_record+=1
            if are_coordinates_close(geocoords_long, geocoords_lat, lat_deg,long_deg):
                found_count += 1
                print("TRUE")
                print("Coordinates are close.")
                break
                
            else:
                not_found_count += 1
                print("Coordinates are not close.")
    print("Total comparisons : ",total_record)
    print("Matches : ",found_count)
    print("No matches : ",not_found_count)

    

