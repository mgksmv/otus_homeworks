from config.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testpostgres',
        'USER': 'testpostgres',
        'PASSWORD': 'testpostgres',
        'HOST': 'testdb',
        'PORT': 5432,
    }
}
