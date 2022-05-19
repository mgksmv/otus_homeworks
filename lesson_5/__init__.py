__all__ = ('app',)

from .models import db, migrate
from .config import app

db.init_app(app)
migrate.init_app(app, db)
