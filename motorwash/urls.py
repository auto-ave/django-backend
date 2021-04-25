from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MotorWash API (All)",
        default_version='v1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("rest/", include("rest_framework.urls", namespace="rest_framework")),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    # path('', include('accounts.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)