
from django.urls import path
from vehicle.views import *

urlpatterns = [
    path('vehicle/type/list/', VehicleTypeListView.as_view(), name="vehicle_type_list"),
    path('vehicle/brands/list/', VehicleBrandsListView.as_view(), name="vehicle_brands_list"),
    path('vehicle/models/list/', VehicleModelsListView.as_view(), name="vehicle_models_list"),
]