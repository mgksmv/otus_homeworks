from config.settings import *

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
