"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
import logging
import json
import mongoengine
from resources.circleci.eb.get_eb_env import patch_environment

# Init logger
logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Patch environment variables
patch_environment()

# Read etc/settings.json
PRODUCTION = False
try:
    if 'QBOTIO_SETTINGS_PATH' in os.environ:
         qbotio_settings_path_env = os.environ['QBOTIO_SETTINGS_PATH']
         json_settings_path = '{}/settings.json'.format(qbotio_settings_path_env)
    else:
        json_settings_path = '{}/etc/settings.json'.format(BASE_DIR)
    with open(json_settings_path) as json_settings:
        JSON_SETTINGS = json.load(json_settings)
        if ('PRODUCTION' in JSON_SETTINGS):
            PRODUCTION = True
            PRODUCTION_SETTINGS = JSON_SETTINGS['PRODUCTION']
except:
    logger.error('Unable to read {}'.format(json_settings_path))
    exit()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = JSON_SETTINGS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'PRODUCTION' not in JSON_SETTINGS

ALLOWED_HOSTS = JSON_SETTINGS['ALLOWED_HOSTS']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'search.apps.SearchConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

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

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': JSON_SETTINGS['DATABASES']['default']
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')
STATIC_URL = '/static/'

# CORS Configuration
CORS_ORIGIN_WHITELIST = JSON_SETTINGS['CORS_ORIGIN_WHITELIST']

# MongoDB Connection
if ('repository' in JSON_SETTINGS['DATABASES']):
    defaultDB = JSON_SETTINGS['DATABASES']['repository']
    mongoengine.connect(
        db=defaultDB['NAME'],
        username=defaultDB['USER'],
        password=defaultDB['PASSWORD'],
        host=defaultDB['HOST'],
        port=defaultDB['PORT']
    )

# Configure Server Error reporting (used in production)
if (PRODUCTION):
    ADMINS = PRODUCTION_SETTINGS['ADMINS']
    SERVER_EMAIL = PRODUCTION_SETTINGS['SERVER_EMAIL']
    EMAIL_HOST = PRODUCTION_SETTINGS['EMAIL_HOST']
    EMAIL_HOST_USER = PRODUCTION_SETTINGS['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = PRODUCTION_SETTINGS['EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = PRODUCTION_SETTINGS['EMAIL_USE_TLS']

# Disables require slash after requests
APPEND_SLASH=False
