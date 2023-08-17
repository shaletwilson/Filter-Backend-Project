# filter/urls.py
from django.urls import path
from . import views
from .views import Login, FlightListCreateView, FlightDetailView, Filter_API_View


app_name = 'filter'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('flight-list/', FlightListCreateView.as_view(), name='flight-list'),
    path('import/', views.import_data, name='import_data'),
    path('flight-detail/<int:id>/', FlightDetailView.as_view(), name='flight-detail'),
    path('filter-api/', Filter_API_View.as_view(), name='filter-api'),
]
