# exchange-rates-app

CONSIDERATIONS/ASSUMPTIONS:
-------------------------------

- in business scenario I will go for adapting something like 
this: https://github.com/evonove/django-money-rates to my needs, but 
I understand you need some coding demonstration.

- base currency for project is setup in settings in `BASE_CURRENCY`

- we use DRF, because it helps making clean API's for Django

- we ignore fact like asking for exchange rate at certain date. 
We keep only one value which we assume is always up-to-date.

- the management command `update_rates` is scrapping fresh currency from ECB

- in production environment one should setup e.g cron job which will 
automatically once per day (on weekdays) at 16 UTC (crontab code `0 16 * * 1-5`) because ECB
 claims updates around 16:00 CET (15 UTC) on every working day. (UTC is CET-1)
 
- I decided to parse static XML served by ECB under 
`https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml`


HOW TO RUN IT
--------------

OS X install:

    hombrew install python3

using hombrew python and pipenv may cause problems when locale not set, so please export:

    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8

create pipenv with:

    pipenv --python /usr/local/Cellar/python/3.7.0/bin/python3

activate virtual environment by:

    pipenv shell

install packages by

    pipenv install

run migrations
==============

    python manage.py migrate


scrape currencies from ECB
==========================

    python manage.py update_rates

web server
==========

run django development server by:

    python manage.py runserver

and go in web browser to the:

    http://127.0.0.1:8000/api/convert/PLN/CHF/200/


Testing
=======

to run this few unit and integration tests, just type in projects directory:

    pytest -v