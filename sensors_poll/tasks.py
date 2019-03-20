from __future__ import absolute_import, unicode_literals
from .celery import app, poll_config

from .poll import SensorPoll


@app.task
def poll_sensors_task():
    SensorPoll(**poll_config).run()
