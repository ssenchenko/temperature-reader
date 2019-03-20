# Parity Test

## Environment description

* Houses have rooms and rooms __can__ have lights that can be controlled individually
* Each house __has a__ furnace. The furnace can either be
  * off,
  * fan-on,
  * heat
* Each room __can__ have sensors used for monitoring.
* Sensors can be for indor temperature, humidity, outdoor temperature.
 For this task only indor temperature task matter.
* Sensors are linked to a 3rd party API that exposes the latest sensor reading every __5 minutes__,
 the historic data for each of these sensors __is NOT stored on the remote source__
* Sensor API <https://api-staging.paritygo.com/sensors/api/sensors/>

## Requirements for API

* get information about a given house and rooms;
* change the furnace state;
* turn lights on and off;
* view historic sensor data for the past __15 minutes__.

## Assumptions

* App is running in the house itself to have access to the furnace and lights switchers
* It means that hardware resources are limited
* Intensive use of network connections, to store / retrieve data to / from a cloud based database
may or may not be the option
* Any services and scripts which are supposed to sync / backup / clean sensor data history, loggs or
 other stored info are out of scope for the test purpose.
* A sensor type has only one metric to measure (according to the API provided).
* Sensors and lights can be outside the house, we put them into 'outside' room.
* We maintain sensor slugs to be equal to slugs from the third party API.
 If a new sensor comes in API, we'll see it in the errors log.
 Mapping of sensor slugs is out of scope.

## Architecture

* 2 services to separate concerns:
  * Home API - Django ORM, Django*REST
    * get information about a given house and rooms;
    * change the furnace state;
    * turn lights on and off;
    * view historic sensor data for the past 15 minutes.
  * Sensors Poll - Requests, Celery, Redis
    * fires every 5 min
    * polls sensor API
    * calls Home API to store sensor data
* SQLite is used for a local database, because of described assumptions
* Daily, another service should sync any data, we need from our local snapshot db, to the cloud
 based db and clear local db. According to made assumptions, it's out of scope.
* Historic sensor data always shows the last data obtained from sensors API and all data which is 15 min older than the last loaded data. It matters, if data is not inserted every 5 min.
* Auth:
  * 3 types of auth are enabled: JWT, Session, and Basic; Basic enabled __only__ for testing API
   with a browser;
  * JWT refresh is not used to simplify client and do not persist / refresh token (which could've
   been another celery task)

## Setup and run

Both apps `home` and `sensors_poll` have `requirements.txt` files to run installation.

All files outside apps folders are required only for development. For example, `requirements.dev.local.txt` has contains dependencies like pylint and yapf.

### `home` app

1. Run migration `pythom manage.py migrate`
2. Load fixture `python manage.py loaddata ./api/fixtures/house-plan.yaml`
3. Create admin user (any name is okay) `python manage.py createsuperuser --email admin@example.com --username admin`
4. Run server `python manage.py runserver`
5. Visit `http://localhost:8000/admin/` for admin interface, use the user you created to log in
6. Visit `http://localhost:8000/api/docs/` to explore Home API
7. You can check also `http://localhost:8000/api/schema/` and start testing at `http://localhost:8000/api/`
8. When done, stop server with Ctrl+C

### `sensors_poll`

1. You need to have redis running on port 6379 to be able to run celery.
2. Rename `poll.ini.example` to `poll.ini`, open it and insert there username and password you chose when set up `home` app
3. Start beat and worker from the directory which contains `sensors_poll` folder with command `celery -A sensors_poll worker -B --loglevel=info` (feel free to change loglevel)
4. When done, stop celery with Ctrl+C
