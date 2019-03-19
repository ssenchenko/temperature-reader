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
 If new sensor comes in API, we'll see it in the errors log. Mapping between sensors is out of scope

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
