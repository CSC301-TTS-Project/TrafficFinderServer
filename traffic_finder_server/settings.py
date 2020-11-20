"""
Django settings for traffic_finder_server project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import configparser
import os
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = os.environ.get('DJANGO_SECRET')
if not SECRET_KEY:
    SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not 'PROD' in os.environ

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'corsheaders',
    'django_nose',
    'django.contrib.gis',
    'api',
    'rest_framework'
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'traffic_finder_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'traffic_finder_server.wsgi.application'

api_log_handler = {
    "level": "DEBUG",
    "class": "logging.StreamHandler"
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if 'CLOUD_BUILD' in os.environ:
    # environment variables loaded in from aws secrets manager
    from .secrets import get_secrets_dict

    secrets = get_secrets_dict()
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': secrets['RDS_TRAFFIC_FINDER_DB'],
            'TEST': {
                # since it's readonly anyways, don't need to copy into a new db
                'NAME': secrets['RDS_TRAFFIC_FINDER_DB']
            },
            'USER': secrets['RDS_USERNAME'],
            'PASSWORD': secrets['RDS_PASSWORD'],
            'HOST': secrets['RDS_HOST'],
            'PORT': secrets['RDS_PORT']
        }
    }
    DDB_ENDPOINT = None

    # Hardcoded for now
    DEFAULT_DDB_USER_ID = "USER"
    DEFAULT_ROUTE = 0

    if "PROD" in os.environ:
        DDB_ROUTE_TABLE_NAME = secrets["DDB_ROUTE_TABLE_NAME"]
        DDB_SEGMENT_TABLE_NAME = secrets["DDB_SEGMENT_TABLE_NAME"]

        api_log_handler = {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/opt/python/log/api.log",
            "formatter": "verbose"
        }
    else:
        DDB_ROUTE_TABLE_NAME = secrets["DDB_TEST_ROUTE_TABLE_NAME"]
        DDB_SEGMENT_TABLE_NAME = secrets["DDB_TEST_SEGMENT_TABLE_NAME"]

    HERE_PUBLIC_KEY = secrets['HERE_PUBLIC_KEY']
    MAPBOX_PUBLIC_KEY = secrets['HERE_PUBLIC_KEY']
else:
    # Read Local Config
    config = configparser.ConfigParser()
    config.read('traffic_finder_server/config/local.ini')
    DATABASES = {
        'default': {
            # DEFAULT TO LOCAL POSTGRES
            # SETUP YOUR OWN LOCAL DB
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': config['POSTGRES']['NAME'],
            'TEST': {
                # since it's readonly anyways, don't need to copy into a new db
                'NAME': config['POSTGRES']['NAME']
            }
        }
    }
    DDB_ENDPOINT = str(config['DYNAMO_DB']['ENDPOINT'])
    DEFAULT_DDB_USER_ID = config['DYNAMO_DB']['DEFAULT_USER_ID']
    DEFAULT_ROUTE = int(config['DYNAMO_DB']['DEFAULT_ROUTE'])
    DDB_ROUTE_TABLE_NAME = config['DYNAMO_DB']['DDB_ROUTE_TABLE_NAME']
    DDB_SEGMENT_TABLE_NAME = config['DYNAMO_DB']['DDB_SEGMENT_TABLE_NAME']

    HERE_PUBLIC_KEY = str(os.environ[config['API_KEYS']['MAPBOX_ENV_VAR']])
    MAPBOX_PUBLIC_KEY = str(os.environ[config['API_KEYS']['MAPBOX_ENV_VAR']])

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s %(levelname)s %(module)s: %(message)s"}
    },
    "handlers": {
        "api_logs": api_log_handler
    },
    "loggers": {
        "api_logs": {"handlers": ["api_logs"], "level": "DEBUG", "propagate": True}
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = False

CORS_ORIGIN_ALLOW_ALL = True
