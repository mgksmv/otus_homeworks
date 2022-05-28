__all__ = ('db', 'migrate', 'User', 'Blog', 'Tag', 'Comment')

from .database import db, migrate
from .all_models import User, Blog, Tag, Comment
