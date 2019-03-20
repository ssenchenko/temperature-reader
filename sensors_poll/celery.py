from __future__ import absolute_import, unicode_literals

import configparser
import logging
import os

from celery import Celery
from celery.signals import after_setup_logger

logger = logging.getLogger(__name__)

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


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter(
        '[%(levelname)] [%(asctime) %(module) %(process:d) %(thread:d)] %(message)')

    # FileHandler
    fh = logging.FileHandler('celery.log')
    fh.setLevel(logging.ERROR)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # StreamHandler
    sh = logging.StreamHandler()
    sh.setLevel(logging.ERROR)
    sh.setFormatter(formatter)
    logger.addHandler(sh)


config = configparser.ConfigParser()
path = os.path.dirname(__file__)
ini_file = os.path.join(path, 'poll.ini')
config.read_file(open(ini_file))
poll_config = {
    'source_url': config['SensorsAPI']['source_url'],
    'target_url_root': config['HomeAPI']['target_url_root'],
    'data_endpoint': config['HomeAPI']['data_endpoint'],
    'auth_endpoint': config['HomeAPI']['auth_endpoint'],
    'username': config['HomeAPI']['username'],
    'password': config['HomeAPI']['password'],
}

if __name__ == '__main__':
    app.start()
