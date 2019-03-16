from django.db import models

import autoslug
import model_utils
import model_utils.fields

# According to https://code.djangoproject.com/ticket/4136
# 2 years ago ModelForm is made to save empty values for nullable CharFields as NULL
# However the ticket to change documentation is still open.
# https://code.djangoproject.com/ticket/28009


class House(models.Model):
    address = models.CharField(
        max_length=50,
        unique=True,
        help_text='For info purposes only. Maybe useful in a cloud db where all houses are stored')

    def __str__(self):
        return self.address


class Furnace(models.Model):
    """
    Furnace is something which heats the house.

    It can have 3 states: off, fan-on, and heat
    Furnace and House has 1:1 relation.
    But what if a house with 2 furnaces happen? It's safer to keep it as separate entity.
    """
    STATUS = model_utils.Choices('OFF', 'FAN', 'HEAT')

    house = models.ForeignKey('House', on_delete=models.CASCADE)
    status = model_utils.fields.StatusField(default=STATUS.OFF)

    def __str__(self):
        return f'Furnace {self.id} at {self.house}'


class Room(models.Model):
    """
    Rooms in the house.

    To describe a room give it a 'name', but don't get too verbose.
    Example: 'floor 2, bedroom' -- OK
             'bedroom on the 2nd floor with a seaside view' -- WRONG, more than 30 symbols
    If you need more details, use 'description' field.
    Slug uses name. The main difference is that there is a unique index imposed on slug.
    AutoSlugField will fix name uniqueness problem silently by adding -1, -2 etc
    """

    house = models.ForeignKey('House', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    slug = autoslug.AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name


class Light(models.Model):
    """
    Lights in the room.

    To create a light source in the room, give it a 'name'.
    If no name given, default 'lights' is profided.
    AutoSlugField will fix name uniqueness problem silently by adding -1, -2 etc
    Light can be ON and OFF.
    """
    STATUS = model_utils.Choices('ON', 'OFF')

    name = models.CharField(max_length=30, default='lights')
    slug = autoslug.AutoSlugField(populate_from='name', unique=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    status = model_utils.fields.StatusField(default=STATUS.OFF)

    def __str__(self):
        return f'{self.name} in the {self.room}'


class SensorType(models.Model):
    """
    Types of the sensors with their units of measure.
    """
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    slug = autoslug.AutoSlugField(populate_from='name', unique=True)
    display_symbol = models.CharField(max_length=5, help_text='Unit of measure')

    def __str__(self):
        return f'{self.name} sensor'

    class Meta:
        db_table = 'api_sensor_type'


class Sensor(models.Model):
    """
    Sensors which can be in a room or outside house.

    We may not know the exact place of the sensor.
    Sensors data come from the third party API, hence it's important to maintain 'provided_slug'
    to be equal to the slugs in the API.
    If we need to add a sensor which is not in the 3rd party API, 'provided_slug' can be null.
    To add more info on the sensor, fill in name and description.
    For example:
        name='humidity inside'
        description='humidity sensor in the basement on the northern wall'
    Slug is used for internal lookups, not connected to the third party API.
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, null=True, blank=True)
    provided_slug = models.CharField(max_length=50, null=True, blank=True, unique=True)
    slug = autoslug.AutoSlugField(populate_from='name', unique=True)
    sensor_type = models.ForeignKey('SensorType', on_delete=models.PROTECT)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.room:
            return f'{self.name} sensor in the {self.room}'
        return f'{self.name} sensor'


class SensorData(models.Model):
    """
    History of sensor data.
    """
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE)
    value = models.FloatField()
    # because values in history got updated only once per 5 min,
    # there is no need to save original timestamp, as soon as we pull them every 5 min
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_sensor_data'
