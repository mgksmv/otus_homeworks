from pytest import fixture, mark
from sqlalchemy.orm import Session as SessionType

from lesson_4.sqlite.db_settings import Session
from lesson_4.sqlite.crud import create_tables, drop_tables, create_user, create_post, create_tag
from lesson_4.sqlite.models import User, Post, Tag


@fixture
def session():
    return Session()


@fixture(scope='session', autouse=True)
def test_db():
    create_tables()
    session = Session()
    yield session
    session.close()
    drop_tables()


class TestBlog:
    # @mark.parametrize('username, email', [
    #     ('1', '1@email.com'),
    #     ('2', '2@email.com'),
    #     ('3', '3@email.com'),
    # ])
    # def test_create_users(self, session: SessionType, test_db, username, email):
    #     new_user = create_user(session, username, email)
    #     all_users = session.query(User).count()
    #     assert all_users == 3

    def test_create_users(self, session: SessionType, test_db):
        data = {
            'goose': 'goose@email.com',
            'duck': 'duck@email.com',
            'swan': 'swan@email.com',
        }
        for username, email in data.items():
            new_user = create_user(session, username, email)
        count_all_users = session.query(User).count()
        assert count_all_users == 3

    def test_get_user(self, session: SessionType, test_db):
        user = session.get(User, 1)
        assert user.id == 1

    def test_create_tags(self, session: SessionType, test_db):
        tag_names = ['sport', 'animals', 'music', 'birds']
        for tag_name in tag_names:
            new_tag = create_tag(session, tag_name)
        all_tags = session.query(Tag).all()
        count_all_tags = session.query(Tag).count()
        assert count_all_tags == 4
        assert all_tags[0].name == 'sport'

    def test_create_posts(self, session: SessionType, test_db):
        data = [
            {
                'id': 1,
                'title': 'honk!',
                'text': 'I am a goose and I can honk!',
                'tag_id': 4
            },
            {
                'id': 2,
                'title': 'quack!',
                'text': 'Hey, the duck is here, stay tuned for more useless info, bye.',
                'tag_id': 4
            },
            {
                'id': 2,
                'title': 'quack!',
                'text': 'Here I am again with another useless blog!',
                'tag_id': 4
            },
            {
                'id': 3,
                'title': 'honk',
                'text': 'Hey. Just hey.',
                'tag_id': 4
            },
        ]
        for info in data:
            new_user = create_post(
                session, user_id=info.get('id'), title=info.get('title'), text=info.get('text'), tag_id=info.get('tag_id')
            )
        count_all_posts = session.query(Post).count()
        assert count_all_posts == 4

    def test_get_user_posts(self, session: SessionType, test_db):
        posts = session.query(Post).filter_by(user_id=2)
        assert posts[0].title == 'quack!'
        assert posts[0].text == 'Hey, the duck is here, stay tuned for more useless info, bye.'
        assert posts[1].title == 'quack!'
        assert posts[1].text == 'Here I am again with another useless blog!'
        assert posts.count() == 2
