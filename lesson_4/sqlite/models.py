from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from lesson_4.sqlite.db_settings import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(32), nullable=False)
    email = Column(String(32), unique=True, nullable=False)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)

    def __str__(self):
        return f'Username: {self.username}\nEmail: {self.email}'

    def __repr__(self):
        return str(self)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer(), primary_key=True)
    name = Column(String(32), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(Text(), nullable=False)
    tag_id = Column(ForeignKey('tags.id'), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)

    user = relationship('User', backref='posts')

    def __str__(self):
        return f'{self.title} by {self.user.username}: {self.text}'

    def __repr__(self):
        return str(self)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer(), primary_key=True)
    text = Column(String(255), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)

    def __str__(self):
        return self.text

    def __repr__(self):
        return str(self)
