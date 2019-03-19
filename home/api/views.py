import datetime as dt

from django.db import models as db
from rest_framework import generics, mixins, viewsets

import api.models
import api.serializers


class ListRetrieveUpdateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin, viewsets.GenericViewSet):
    pass


class FurnaceViewSet(ListRetrieveUpdateViewSet):
    queryset = api.models.Furnace.objects.all()
    serializer_class = api.serializers.FurnaceSerializer


class LightsViewSet(ListRetrieveUpdateViewSet):
    lookup_field = 'slug'
    queryset = api.models.Light.objects.select_related('room').all()
    serializer_class = api.serializers.LightsSerializer


class HouseView(generics.ListAPIView):
    queryset = api.models.House.objects.all()
    serializer_class = api.serializers.HouseSerializer


class SensorDataView(generics.ListCreateAPIView):
    DELTA_MINUTES = 14  # not 15 bc we deal with DateTime and seconds

    serializer_class = api.serializers.SensorDataSerializer

    def get_queryset(self):
        # annotate & order_by desc instead of aggregate & Max to make it work with Subquery
        # aggregate returns a dict which doesn't work with Subquery
        # doesn't hit db while aggregate hits it immediately
        max_stamp = api.models.SensorData.objects.annotate(
            max_stamp=db.ExpressionWrapper(
                db.F('timestamp') - dt.timedelta(minutes=self.DELTA_MINUTES),
                output_field=db.DateTimeField())).order_by('-max_stamp').values('max_stamp')[:1]
        # doesn't hit db
        dataset = api.models.SensorData.objects.filter(timestamp__gt=db.Subquery(max_stamp))
        return dataset
