MOJ open-data-platform
======================

A simplistic application to store open data, APIs and applications


Running locally
---------------

- check out this repository
- make sure you have python, pip and postgresql installed
- run:

    `cd open-data-platform`

    `pip -r requirements.txt`

- create a postgresql database
- set the following environment variables (adapt as needed):

    `export DATABASE_URL=postgres://dbuser:dbpassword@localhost:port/dbname`
    `export MOJOD_DEBUG=True`
    `export MOJOD_TEMPLATE_DEBUG=True`
    `export MOJOD_STATIC_ROOT=/tmp/static`

If you want to set a password:

    `export MOJOD_BASIC_WWW_AUTHENTICATION_USERNAME="user"`
    `export MOJOD_BASIC_WWW_AUTHENTICATION_PASSWORD="password"`
    `export MOJOD_BASIC_WWW_AUTHENTICATION=True`


- initalise the application:

    `python manage.py schemamigration download --initial`

    `python manage.py migrate download`

    `python manage.py syncdb`

- run the application

    `python manage.py runserver`


Running on heroku
-----------------

Follow the [instructions](https://devcenter.heroku.com/articles/getting-started-with-django) on the heroku site. Before the `heroku ps:scale web=1` command, type:

    heroku config:set \
    DJANGO_SETTINGS_MODULE=data_justice.settings \
    DATABASE_URL=postgres://dbuser:dbpassword@localhost:port/dbname \
    MOJD_ALLOWED_HOST="*" \
    MOJD_STATIC_ROOT=staticfiles

if you want to set a password:

    heroku config:set \
    MOJOD_BASIC_WWW_AUTHENTICATION_USERNAME="user" \
    MOJOD_BASIC_WWW_AUTHENTICATION_PASSWORD="password" \
    MOJOD_BASIC_WWW_AUTHENTICATION=True

and then:

    heroku run python manage.py syncdb --all
