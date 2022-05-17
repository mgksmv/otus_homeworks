__all__ = ('app',)

from flask import Flask
from decouple import config

app = Flask(__name__, static_folder='static')
app.config.update(
    ENV=config('ENV'),
    SECRET_KEY=config('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=config('SQLALCHEMY_DATABASE_URI'),
    MAIL_SERVER=config('MAIL_SERVER'),
    MAIL_PORT=config('MAIL_PORT'),
    MAIL_USE_TLS=config('MAIL_USE_TLS'),
    MAIL_USE_SSL=config('MAIL_USE_SSL'),
    MAIL_USERNAME=config('MAIL_USERNAME'),
    MAIL_PASSWORD=config('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=config('MAIL_DEFAULT_SENDER'),
)
