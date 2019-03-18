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
    queryset = api.models.SensorData.objects.all()
    serializer_class = api.serializers.SensorDataSerializer
