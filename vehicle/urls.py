
from django.urls import path
from vehicle.views import *

urlpatterns = [
    path('vehicle/type/list/', VehicleTypeListView.as_view(), name="vehicle_type_list"),
    path('vehicle/wheel/list/', WheelListView.as_view(), name="vehicle_wheel_list"),
    path('vehicle/brand/list/', VehicleBrandsListView.as_view(), name="vehicle_brands_list"),
    path('vehicle/model/list/', VehicleModelsListView.as_view(), name="vehicle_models_list"),
    path('vehicle/model/from-reg/', VehicleModelFromRegView.as_view(), name="vehicle_model_from_reg"),
    
    
    
    ## IRELAND URLS
    path('ie/vehicle/type/list/', VehicleTypeListView.as_view(), name="vehicle_type_list"),
    path('ie/vehicle/wheel/list/', WheelListView.as_view(), name="vehicle_wheel_list"),
    path('ie/vehicle/brand/list/', VehicleBrandsListView.as_view(), name="vehicle_brands_list"),
    path('ie/vehicle/model/list/', VehicleModelsListView.as_view(), name="vehicle_models_list"),
    path('ie/vehicle/model/from-reg/', VehicleModelFromRegView.as_view(), name="vehicle_model_from_reg"),
]