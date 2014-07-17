MOJ open-data-platform
======================

A simplistic application to store open data, APIs and applications


Running locally
---------------

Check out this repository.

Make sure you have python, pip and postgresql installed.

Run:

    cd open-data-platform
    pip -r requirements.txt

Create a postgresql database

Set the following environment variables (adapt as needed):

    export DATABASE_URL=postgres://dbuser:dbpassword@localhost:port/dbname
    export MOJOD_DEBUG=True
    export MOJOD_TEMPLATE_DEBUG=True
    export MOJOD_STATIC_ROOT=/tmp/static

If you want to set a password:

    export MOJOD_BASIC_WWW_AUTHENTICATION_USERNAME="user"
    export MOJOD_BASIC_WWW_AUTHENTICATION_PASSWORD="password"
    export MOJOD_BASIC_WWW_AUTHENTICATION=True

Initalise the application:

    python manage.py schemamigration download --initial
    python manage.py migrate download
    python manage.py syncdb

Run the application:

    Python manage.py runserver


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

Outcome database
----------------

The application needs to connect to a database that contains the outcomes and other data (court names, offense descriptions, etc). The site will work without that database, but it won't offer the most useful features.

If such a database is set up, its credentials should be set as:

    MOJOD_OUTCOMES_DB_URL=postgres://dbuser:dbpassword@localhost:port/dbname


The database schema is pretty much self explanatory, but more details can be found in the way it's used in the code (see [models.py](tree/master/home/models.py) and [views.py](tree/master/home/views.py).

Obtaining or building the outcomes database
-------------------------------------------

The outcomes database contains not only a table to record all the outcomes, but also other tables to interpret the codes found in the outcomes (eg pleas, offences, etc.). Those tables are built from the spreadsheet that accompany the dataset. Each table in the spreadsheet is converted into a CSV file that is then inserted in a database table.

Some of those CSV tables are available in [a static directory](tree/master/home/static) of this repo. Typically, they would be imported into the database as follows:

    psql -h dbhost -p dbport -W --dbname dbname --username user
    create table offences (lookup integer, act varchar(1024), section varchar(1024), description varchar(1024), magsmaxsentence varchar(255),magsclasstrial varchar(255),magsclassunder18 varchar(255),magsclassover18 varchar(255), crownmaxsentence varchar(255),crownclasstrial varchar(255),crownclassconvlower varchar(255),crimsec3 varchar(255),yearinsertcodebooks varchar(255), id integer PRIMARY KEY);
    \copy offences(lookup, act, section, description, magsmaxsentence, magsclasstrial, magsclassunder18, magsclassover18, crownmaxsentence, crownclasstrial, crownclassconvlower, crimsec3, yearinsertcodebooks) from '/tmp/offense-classifications.csv' delimiter ',' csv header

We will soon release a full postgresql dump.


