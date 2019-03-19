from django.urls import include, path
from rest_framework import routers, schemas
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

import api.views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'lights', api.views.LightsViewSet)
ROUTER.register(r'furnaces', api.views.FurnaceViewSet)
ROUTER.register(r'sensor-data', api.views.SensorDataViewSet, basename='sensor-data')
ROUTER.register(r'status', api.views.HouseViewSet)
# ROUTER.register(r'sensor-data', api.views.SensorDataViewSet, basename='sensor-data')

TITLE = 'Home API'
SCHEMA_VIEW = schemas.get_schema_view(title=TITLE)
DOCS_VIEW = include_docs_urls(title=TITLE, public=False)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('token-auth/', obtain_jwt_token),
    path('docs/', DOCS_VIEW),
    path('schema/', SCHEMA_VIEW),
    path('', include(ROUTER.urls)),
]
