
from django.urls import path
from vehicle.views import *

urlpatterns = [
    path('vehicle/type/list/', VehicleTypeListView.as_view(), name="vehicle_type_list"),
    path('vehicle/wheel/list/', WheelListView.as_view(), name="vehicle_wheel_list"),
    path('vehicle/brand/list/', VehicleBrandsListView.as_view(), name="vehicle_brands_list"),
    path('vehicle/model/list/', VehicleModelsListView.as_view(), name="vehicle_models_list"),
]