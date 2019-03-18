from django.urls import include, path
from rest_framework import routers, schemas
from rest_framework.documentation import include_docs_urls

import api.views

ROUTER = routers.DefaultRouter()
ROUTER.register(r'lights', api.views.LightsViewSet)
ROUTER.register(r'furnaces', api.views.FurnaceViewSet)
# ROUTER.register(r'sensor-data', api.views.SensorDataViewSet, basename='sensor-data')

TITLE = 'Home API'
SCHEMA_VIEW = schemas.get_schema_view(title=TITLE)

urlpatterns = [
    path('docs/', include_docs_urls(title=TITLE, public=False)),
    path('schema/', SCHEMA_VIEW),
    path('status/', api.views.HouseView.as_view()),
    path('', include(ROUTER.urls)),
    path('sensor-data/', api.views.SensorDataView.as_view())
]
