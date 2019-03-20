from django.contrib import admin

from api import models

admin.site.register(models.House)
admin.site.register(models.Furnace)
admin.site.register(models.Room)
admin.site.register(models.Light)
admin.site.register(models.SensorType)
admin.site.register(models.Sensor)
