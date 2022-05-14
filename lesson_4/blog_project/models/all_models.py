from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin

from .database import db

Base = declarative_base()

bookmarks = db.Table('bookmarks',
                     db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id')),
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                     )

blog_tags = db.Table('blog_tags',
                     db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='SET NULL'))
                     )


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    bio = db.Column(db.String(255))
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bookmarks = relationship('Blog', secondary=bookmarks, lazy='subquery', backref=db.backref('pages', lazy=True))
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    def __str__(self):
        return self.username

    def __repr__(self):
        return str(self)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    color = db.Column(db.String(6), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    tags = relationship('Tag', secondary=blog_tags)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)

    user = relationship('User', backref='posts')
    comments = relationship('Comment', backref='comments')

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.ForeignKey('blogs.id'), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)

    user = relationship('User', backref='comments')

    def __str__(self):
        return self.text

    def __repr__(self):
        return str(self)
