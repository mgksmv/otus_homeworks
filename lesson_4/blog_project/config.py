__all__ = ('app',)

from flask import Flask

app = Flask(__name__, static_folder='static')
app.config.update(
    ENV='development',
    SECRET_KEY='qwaszx784512',
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:890213@localhost:5432/blog',
    SQLALCHEMY_ECHO=False,
    MAIL_SERVER=YOUR_MAIL_SERVER,
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=YOUR_MAIL_USERNAME,
    MAIL_PASSWORD=YOUR_MAIL_PASSWORD
    MAIL_DEFAULT_SENDER=YOUR_DEFAULT_SENDER,
)
