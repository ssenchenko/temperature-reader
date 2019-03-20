import requests
import logging

logger = logging.getLogger(__name__)


class SensorPoll:

    def __init__(self, **config):
        self.source_url = config['source_url']
        self.target_auth_url = config['target_url_root'] + config['auth_endpoint']
        self.target_data_url = config['target_url_root'] + config['data_endpoint']
        self.username = config['username']
        self.password = config['password']

    def poll_sensors(self):
        """
        Poll sensors API.

        :rtype: [{
            'name': str,
            'slug': str,
            'value': float,
            'sensor_type': str,
            'timestap': str,
            'display_symbol': str}]
        """
        response = requests.get(self.source_url)
        response.raise_for_status()  # if it was 4XX or 5XX
        result = response.json()
        return result

    @staticmethod
    def transform(sensors_data):
        """
        Transform data from sensor API to Home API format.

        :param sensors_data: [{
            'name': str,
            'slug': str,
            'value': float,
            'sensor_type': str,
            'timestap': str,
            'display_symbol': str}]
        :rtype: generator({
            'sensor': str,
            'value': float})
        """
        for data_item in sensors_data:
            yield {
                'sensor': data_item['slug'],
                'value': data_item['value'],
            }

    def post_to_home(self, data_item, session=None):
        """
        Create sensor data item.

        :param data_item: {
            'sensor': str,
            'value': float}
        :param session: requests.Session, to use session auth settings and connection pool
        """
        post_func = session.post if session else requests.post
        response = post_func(self.target_data_url, data=data_item)
        response.raise_for_status()  # if it was 4XX or 5XX

    def get_auth_token(self, session=None):
        """
        Obtain JWT token.

        :param session: requests.Session, to use session auth settings and connection pool, optional
        :rtype: {'token': 'XXXXXXX'}
        """
        post_func = session.post if session else requests.post
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = post_func(self.target_auth_url, data=data)
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    def append_token_to_session(session, token):
        """
        Append auth token to the session header.

        :param session: requests.Session
        :param token: {'token': 'XXXXXXX'}
        """
        session.headers.update({'Authorization': f"JWT {token['token']}"})

    def run(self):
        """
        Poll sensor API, transfor result to home API format, and post.
        """
        try:
            sensors_data = self.poll_sensors()
        except requests.exceptions.HTTPError as err:
            logger.error(f'Polling Sensors API error: {err}')
        except requests.exceptions.ConnectionError as err:
            logger.error(f'Cannot connect to Sensors API: {err}')
        else:
            with requests.Session() as session:
                try:
                    token = self.get_auth_token(session)
                except requests.exceptions.HTTPError as err:
                    logger.error(f'Auth error: {err}')
                except requests.exceptions.ConnectionError as err:
                    logger.error(f'Cannot connect to Home API: {err}')
                else:
                    self.append_token_to_session(session, token)
                    for data_item in self.transform(sensors_data):
                        try:
                            self.post_to_home(data_item, session)
                        except requests.exceptions.HTTPError as err:
                            logger.error(f'Sensor data insertion error: {err}')
