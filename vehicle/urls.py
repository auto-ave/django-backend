
from django.urls import path
from vehicle.views import *

urlpatterns = [
    path('vehicle_type/list/', VehicleTypeListView.as_view(), name="vehicle_type_list")
]