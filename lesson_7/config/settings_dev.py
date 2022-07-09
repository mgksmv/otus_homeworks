from config.settings import *

# Local testing

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testpostgres',
        'USER': 'testpostgres',
        'PASSWORD': 'testpostgres',
        'HOST': 'localhost',
        'PORT': 5433,
    }
}


# Docker

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'testpostgres',
#         'USER': 'testpostgres',
#         'PASSWORD': 'testpostgres',
#         'HOST': 'testdb',
#         'PORT': 5432,
#     }
# }
