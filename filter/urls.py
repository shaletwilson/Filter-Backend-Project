# filter/urls.py
from django.urls import path
from . import views
from .views import Login, FlightListCreateView, FlightDetailView, Filter_API_View, TestView, AirportListView


app_name = 'filter'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('flight-list/', FlightListCreateView.as_view(), name='flight-list'),
    # path('import/', views.import_data, name='import_data'),
    path('import-airport-data/', views.import_airport_data, name='import-airport-data'),
    path('flight-detail/<int:id>/', FlightDetailView.as_view(), name='flight-detail'),
    path('single-filter-api/', Filter_API_View.as_view(), name='single-filter-api'),
    path('filter-api/', TestView.as_view(), name='filter-api'),
    # path('test-api/', TestView.as_view(), name='test-api'),

    path('airport-list-api/', AirportListView.as_view(), name='airport-list-api'),
]
