from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import declarative_base

DB_URL = "postgresql+pg8000://admin:890213@localhost:5432/blog"
DB_ECHO = True
engine = create_engine(url=DB_URL, echo=DB_ECHO)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(32), nullable=False)
    email = Column(String(32), unique=True, nullable=False)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer(), primary_key=True)
    name = Column(String(32), nullable=False)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(Text(), nullable=False)
    tag_id = Column(ForeignKey('tags.id'), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer(), primary_key=True)
    text = Column(String(255), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)


def create_tables():
    Base.metadata.create_all()


if __name__ == '__main__':
    create_tables()
