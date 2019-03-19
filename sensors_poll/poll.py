import requests

SOURCE_URL = 'https://api-staging.paritygo.com/sensors/api/sensors/'
TARGET_URL = 'http://localhost:8000/api/sensor-data/'


def poll_sensors():
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
    response = requests.get(SOURCE_URL)
    response.raise_for_status()  # if it was 4XX or 5XX
    result = response.json()
    return result


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


def post_to_home(data_item):
    """
    Create sensor data item.

    :param data_item: {
        'sensor': str,
        'value': float}
    """
    response = requests.post(TARGET_URL, data=data_item)
    response.raise_for_status()  # if it was 4XX or 5XX


def get_sensor_data():
    """
    Poll sensor API, transfor result to home API format, and post.
    """
    try:
        sensors_data = poll_sensors()
    except requests.exceptions.HTTPError as err:
        print(repr(err))
    else:
        for data_item in transform(sensors_data):
            try:
                post_to_home(data_item)
            except requests.exceptions.HTTPError as err:
                print(repr(err))
