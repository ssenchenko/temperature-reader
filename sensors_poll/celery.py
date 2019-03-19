from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('sensors_poll', broker='redis://localhost:6379/1', include=['sensors_poll.tasks'])

# Optional configuration, see the application user guide.
# app.conf.update(result_expires=3600,)
app.conf.beat_schedule = {
    'poll-sensors-every-5-minute': {
        'task': 'sensors_poll.tasks.poll_sensors_task',
        'schedule': 300.0,  # in seconds
        'args': ()
    },
}
app.conf.timezone = 'America/Toronto'

if __name__ == '__main__':
    app.start()
