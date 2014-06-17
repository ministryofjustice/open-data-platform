open-data-platform
==================

A simplistic application to store open data, APIs and applications


Running locally
---------------

- check out this repository
- make sure you have python, pip and postgresql installed
- run:

    `cd open-data-platform`
    
    `pip -r requirements.txt`

- create a postgresql database
- set the following environment variables:

    `export DATABASE_URL=postgres://dbuser:dbpassword@localhost:port/dbname`
    
- initalise the application:

    `python manage.py schemamigration download --initial`
    
    `python manage.py migrate download`
    
    `python manage.py syncdb`
    
- run the application

    `python manage.py runserver`


Running on heroku
-----------------

Follow the [instructions](https://devcenter.heroku.com/articles/getting-started-with-django) on the heroku site. Before the `heroku ps:scale web=1` command, type:

    `heroku config:set DJANGO_SETTINGS_MODULE=data_justice.settings`
