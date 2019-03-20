from rest_framework import serializers

import api.models


class FurnaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = api.models.Furnace
        fields = (
            'id',
            'status',
        )
        read_only_fields = ('id',)


class RoomLightsSerializer(serializers.ModelSerializer):

    class Meta:
        model = api.models.Light
        fields = (
            'name',
            'slug',
            'status',
        )


class SensorTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = api.models.SensorType
        fields = (
            'name',
            'description',
            'slug',
            'display_symbol',
        )


class SensorSerializer(serializers.ModelSerializer):
    sensor_type = SensorTypeSerializer(read_only=True)

    class Meta:
        model = api.models.Sensor
        fields = (
            'name',
            'description',
            'slug',
            'sensor_type',
        )


class RoomSerializer(serializers.ModelSerializer):
    lights = RoomLightsSerializer(many=True, read_only=True)
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = api.models.Room
        fields = (
            'name',
            'description',
            'slug',
            'lights',
            'sensors',
        )


class HouseSerializer(serializers.ModelSerializer):
    furnaces = FurnaceSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = api.models.House
        fields = (
            'address',
            'furnaces',
            'rooms',
        )


class RoomShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = api.models.Room
        fields = (
            'name',
            'description',
            'slug',
        )


class LightsSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    room = RoomShortSerializer(many=False, read_only=True)

    class Meta:
        model = api.models.Light
        fields = (
            'name',
            'slug',
            'room',
            'status',
        )
        read_only_fields = ('name',)


class SensorDataSerializer(serializers.ModelSerializer):
    sensor = serializers.SlugRelatedField(
        slug_field='slug', queryset=api.models.Sensor.objects.all())

    class Meta:
        model = api.models.SensorData
        fields = (
            'sensor',
            'value',
            'timestamp',
        )
        read_only_fields = ('timestamp',)

    def to_representation(self, instance):
        # Overriding this method, helps to avoid two separate fields for creation and reading.
        # Here both creation and reading can be done by using sensor key.
        response = super().to_representation(instance)
        response['sensor'] = SensorSerializer(instance.sensor).data
        return response
