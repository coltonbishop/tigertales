"""
Django settings for tigertales project.

"""

import os
import dj_database_url
import sys
import urlparse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'tqtl!sopllc8#o74qn*2ak+y4@s$u0pp#_06+9d%b#)9js$ae-'

DEBUG = True

ALLOWED_HOSTS = ['tigertales.herokuapp.com', 'localhost', '127.0.0.1', 'us-cdbr-iron-east-05.cleardb.net']

# emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SENDGRID_API_KEY = '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'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'princetontigertales@gmail.com'
# Use for Heroku (comment out other)
# EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
# EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
#Use for localhost (comment out other)
EMAIL_HOST_USER = 'tigertales'
EMAIL_HOST_PASSWORD = 'princetonCOS333'

# Application definition
INSTALLED_APPS = [
	'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
	'django_cas_ng',
    'gunicorn' ,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'tigertales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

DATABASES = {
	# for Heroku
    # 'default': {
    # 	'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'heroku_76b833d89a9371b',
    #     'HOST': 'us-cdbr-iron-east-05.cleardb.net',
    #     'PORT': '3306',
    #     'USER': 'b55fadbc5ed807',
    #     'PASSWORD': '0b4029ab',    }

	# for Local
    'default': {
    	'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tiger_tales',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'tiger',
        'PASSWORD': 'COS333pton',    }
}

# Password validation
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

AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend'
]

LOGIN_URL = '/app'
LOGOUT_URL = '/app'
CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'
CAS_REDIRECT_URL = '/app' # Points to landing page
CAS_APPLY_ATTRIBUTES_TO_USER = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Vanilla
STATIC_URL = '/static/'
STATICFILES_DIRS = ['/static']
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
