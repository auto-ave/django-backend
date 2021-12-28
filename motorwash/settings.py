"""
Django settings for motorwash project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import datetime, os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


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
    'drf_yasg',
    'django_filters',
    'phonenumber_field',
    'custom_admin_arrayfield',
    'dbbackup',
    'djcelery_email',
    'background_task',
    'fcm_django',
    
    'accounts',
    'common',
    'vehicle',
    'store',
    'booking',
    'misc',
    'cart'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'motorwash.urls'

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

WSGI_APPLICATION = 'motorwash.wsgi.application'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd2dp3lk3a5fd88',
#         'USER': 'ipdsrwgbrteopp',
#         'PASSWORD': '7687ee065748c43a1374bf415be7d9d7b47594e075005d823253522c292ab4df',
#         'HOST': 'ec2-34-204-128-77.compute-1.amazonaws.com',
#         'PORT': '5432',
#     }
# }
if 'RDS_DB_NAME' in os.environ:
    print('Using RDS')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    print('Using local DB')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'motorwash',
            'USER': 'motorwash',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    # Initial Heroku DB, https://motorwash.herokuapp.com
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'd2dp3lk3a5fd88',
    #         'USER': 'ipdsrwgbrteopp',
    #         'PASSWORD': '7687ee065748c43a1374bf415be7d9d7b47594e075005d823253522c292ab4df',
    #         'HOST': 'ec2-34-204-128-77.compute-1.amazonaws.com',
    #         'PORT': '5432',
    #     }
    # }



import dj_database_url 
prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Logging TODO:
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'logs/django.log')
# LOGGING = {
# 	"version": 1,
# 	"disable_existing_loggers": False,
# 	# "formatters": {
# 	# 	"verbose": {"format": "%(asctime)s %(levelname)s %(module)s: %(message)s"}
# 	# },
# 	"handlers": {
# 		"file": {
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': LOG_FILE_PATH,
#             'when': 'midnight',
#             'interval': 1,
#             'backupCount': 1,
#             'encoding': 'utf-8'
#         }
# 	},
# 	"loggers": {
# 		"django": {
#             "handlers": ["file"],
#             "level": LOG_LEVEL, 
#         },
#         # "autoave": {
#         #     "handlers": ["file"],
#         #     "level": LOG_LEVEL, 
#         # }
# 	},
# }

# Django Rest Framework
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # Filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,

    # Thottling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'public_post_api': '3/hour',
        'public_get_api': '100/day' # TODO: yet to be decided
    }
}

# JWT Authentication
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('JWT','Bearer'),
}

# Cross-Origin Resource Sharing (CORS)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "https://moterwash.netlify.app",
#     "https://motorwash-salesman.netlify.app",
#     "https://owner-motorwash.netlify.app",
# ]

CORS_ALLOWED_ORIGIN_REGEXES = [
    "http://localhost:3000",
    "http://localhost:4000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4000",

    "https://moterwash.netlify.app",
    "https://motorwash-salesman.netlify.app",
    "https://owner-motorwash.netlify.app",

    # "https://autoave.care",
    # "https://sales.autoave.care",
    # "https://owner.autoave.care",

    "https://autoave.in",
    "https://sales.autoave.in",
    "https://owner.autoave.in",

]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [
    'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Lauda Paytm
PAYTM_MID = env('PAYTM_MID')
PAYTM_MKEY = env('PAYTM_MKEY')
PAYTM_CURRENCY = env('PAYTM_CURRENCY')

# Email Setup
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "apikey"
# EMAIL_HOST_PASSWORD = ""
# EMAIL_USE_SSL = True

# Firebase Admin
from firebase_admin import initialize_app
from firebase_admin import credentials
cred = credentials.Certificate("/etc/pki/tls/certs/autoave-global-firebase-adminsdk.json")
FIREBASE_APP = initialize_app(cred)
FCM_DJANGO_SETTINGS = {
     # default: _('FCM Django')
    "APP_VERBOSE_NAME": "Autoave Notifications",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
}

# Django Storages
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'motorwash.storage_backends.MediaStorage'


# SendGrid Email
SENDGRID_API_KEY = env('SENDGRID_API_KEY')
SENDGRID_SENDER = env('SENDGRID_SENDER')
