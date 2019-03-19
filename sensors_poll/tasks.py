from __future__ import absolute_import, unicode_literals
from .celery import app

from .poll import get_sensor_data


@app.task
def poll_sensors_task():
    get_sensor_data()
