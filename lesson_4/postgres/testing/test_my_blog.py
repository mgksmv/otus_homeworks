from pytest import fixture, mark
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from lesson_4.postgres.db_settings import Base
from lesson_4.postgres.crud import create_user, create_post, create_tag, create_comment
from lesson_4.postgres.models import User, Post, Tag, Comment


@fixture(scope='session', autouse=True)
def engine():
    return create_engine('postgresql+pg8000://test:test@localhost:5433/test-blog')


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

    @mark.parametrize('title, text', [
        ('honk!', 'I am a goose and I can honk!'),
        ('quack!', 'Hey, the duck is here, stay tuned for more useless info, bye.'),
        ('honk', 'Hey. Just hey.'),
    ])
    def test_create_posts(self, session: Session, title, text):
        new_user = create_user(session, 'goose', 'goose@gmail.com')
        new_tag = create_tag(session, 'birds')
        new_post = create_post(session, user_id=new_user.id, title=title, text=text, tags=[new_tag])
        all_posts = session.query(Post)
        assert new_tag is not None
        assert all_posts.count() == 1
        assert new_post.user_id == new_user.id
        assert new_post.title == title
        assert new_post.text == text

    @mark.parametrize('text', ['wow!', 'nice', 'cool'])
    def test_create_comments(self, session: Session, text):
        new_user = create_user(session, 'goose', 'goose@gmail.com')
        new_comment = create_comment(session, text, new_user.id)
        all_comments = session.query(Comment)
        assert all_comments.count() == 1
        assert new_comment.text == text
        assert new_comment.user_id == new_user.id
