from pytest import fixture, mark
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from lesson_4.postgres.db_settings import Base
from lesson_4.postgres.crud import create_user, create_post, create_tag, create_comment
from lesson_4.postgres.models import User, Post, Tag, Comment


@fixture(scope='session', autouse=True)
def engine():
    return create_engine('postgresql+pg8000://test:test@5433:5432/test-blog')


@fixture(scope='session', autouse=True)
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@fixture
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


class TestBlog:
    @mark.parametrize('username, email', [
        ('goose', 'goose@email.com'),
        ('duck', 'duck@email.com'),
        ('swan', 'swan@email.com'),
    ])
    def test_create_users(self, session: Session, username, email):
        new_user = create_user(session, username, email)
        all_users = session.query(User)
        assert all_users.count() == 1
        assert new_user.username == username
        assert new_user.email == email

    @mark.parametrize('tag_name', ['sport', 'animals', 'music'])
    def test_create_tags(self, session: Session, tag_name):
        new_tag = create_tag(session, tag_name)
        all_tags = session.query(Tag)
        assert all_tags.count() == 1
        assert new_tag.name == tag_name

    @mark.parametrize('user_id, title, text', [
        (1, 'honk!', 'I am a goose and I can honk!'),
        (2, 'quack!', 'Hey, the duck is here, stay tuned for more useless info, bye.'),
        (3, 'honk', 'Hey. Just hey.'),
    ])
    def test_create_posts(self, session: Session, user_id, title, text):
        new_tag = create_tag(session, 'birds')
        new_post = create_post(session, user_id=user_id, title=title, text=text, tags=[new_tag])
        all_posts = session.query(Post)
        assert new_tag is not None
        assert all_posts.count() == 1
        assert new_post.user_id == user_id
        assert new_post.title == title
        assert new_post.text == text

    @mark.parametrize('text, user_id', [
        ('wow!', 1),
        ('nice', 2),
        ('cool', 3),
    ])
    def test_create_comments(self, session: Session, text, user_id):
        new_comment = create_comment(session, text, user_id)
        all_comments = session.query(Comment)
        assert all_comments.count() == 1
        assert new_comment.text == text
        assert new_comment.user_id == user_id
