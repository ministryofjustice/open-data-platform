"""
Django settings for data_justice project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MOJOD_SECRET_KEY', 'dummysecretkey')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('MOJOD_DEBUG', False))

TEMPLATE_DEBUG = bool(os.environ.get('MOJOD_TEMPLATE_DEBUG', False))

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'download.context_processors.globals'
)

ALLOWED_HOSTS = [os.environ.get('MOJOD_ALLOWED_HOST', '')]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'moj_template',
    'download',
    'home',
    'api',
    'apps',
    'feedback',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auth.BasicAuthenticationMiddleware',
)

ROOT_URLCONF = 'data_justice.urls'

WSGI_APPLICATION = 'data_justice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if os.environ.get('DATABASE_URL') == None:
    print 'You must set the DATABASE_URL environment variable. Format: "postgres://username:password@host:port/dbname"'
    sys.exit(-1)

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(),
}

outcomes_database = os.environ.get('MOJOD_OUTCOMES_DB_URL')
if outcomes_database == None:
    print 'Warning! No outcomes database specified. Some site features may not work.'
else:
    DATABASES['outcomes'] = dj_database_url.parse(outcomes_database)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('MOJOD_STATIC_ROOT', '/tmp/static/')

STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static") ]

# List of finder classes that know how to find static files in
# various locations.
#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#)

BASIC_WWW_AUTHENTICATION_USERNAME = os.environ.get('MOJOD_BASIC_WWW_AUTHENTICATION_USERNAME')
BASIC_WWW_AUTHENTICATION_PASSWORD = os.environ.get('MOJOD_BASIC_WWW_AUTHENTICATION_PASSWORD')
BASIC_WWW_AUTHENTICATION = bool(os.environ.get('MOJOD_BASIC_WWW_AUTHENTICATION', False))
