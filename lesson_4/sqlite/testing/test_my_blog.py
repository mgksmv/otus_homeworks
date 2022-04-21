from pytest import fixture, mark, raises
from sqlalchemy.orm import Session as SessionType

from lesson_4.sqlite.db_settings import Session
from lesson_4.sqlite.crud import create_tables, drop_tables, create_user, create_post, create_tag, create_comment
from lesson_4.sqlite.models import User, Post, Tag, Comment


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
    @mark.parametrize('username, email, expected_result', [
        ('goose', 'goose@email.com', 1),
        ('duck', 'duck@email.com', 2),
        ('swan', 'swan@email.com', 3),
    ])
    def test_create_users(self, session: SessionType, test_db, username, email, expected_result):
        new_user = create_user(session, username, email)
        all_users = session.query(User)
        assert all_users.count() == expected_result

    @mark.parametrize('user_id, expected_id, expected_username', [
        (1, 1, 'goose'),
        (2, 2, 'duck'),
        (3, 3, 'swan'),
    ])
    def test_get_user(self, session: SessionType, test_db, user_id, expected_id, expected_username):
        user = session.get(User, user_id)
        assert user.id == expected_id
        assert user.username == expected_username

    @mark.parametrize('tag_name, expected_result', [
        ('sport', 1),
        ('animals', 2),
        ('music', 3),
    ])
    def test_create_tags(self, session: SessionType, test_db, tag_name, expected_result):
        new_tag = create_tag(session, tag_name)
        all_tags = session.query(Tag)
        assert all_tags.count() == expected_result
        assert new_tag.name == tag_name

    def test_create_posts(self, session: SessionType, test_db):
        new_tag = create_tag(session, 'birds')
        data = [
            {
                'id': 1,
                'title': 'honk!',
                'text': 'I am a goose and I can honk!',
                'tag_id': new_tag.id
            },
            {
                'id': 2,
                'title': 'quack!',
                'text': 'Hey, the duck is here, stay tuned for more useless info, bye.',
                'tag_id': new_tag.id
            },
            {
                'id': 3,
                'title': 'honk',
                'text': 'Hey. Just hey.',
                'tag_id': new_tag.id
            },
        ]
        for info in data:
            new_user = create_post(
                session, user_id=info.get('id'), title=info.get('title'), text=info.get('text'), tag_id=info.get('tag_id')
            )
        all_posts = session.query(Post)
        assert all_posts.count() == 3

    @mark.parametrize('user_id, expected_title, expected_text', [
        (1, 'honk!', 'I am a goose and I can honk!'),
        (2, 'quack!', 'Hey, the duck is here, stay tuned for more useless info, bye.'),
        (3, 'honk', 'Hey. Just hey.'),
    ])
    def test_get_user_posts(self, session: SessionType, test_db, user_id, expected_title, expected_text):
        post = session.query(Post).filter_by(user_id=user_id).first()
        all_posts = session.query(Post)
        assert post.title == expected_title
        assert post.text == expected_text
        assert all_posts.count() == 3

    @mark.parametrize('text, user_id, expected_result', [
        ('wow', 3, 1),
        ('nice', 2, 2),
        ('cool', 1, 3),
    ])
    def test_create_comments(self, session: SessionType, test_db, text, user_id, expected_result):
        new_comment = create_comment(session, text, user_id)
        all_comments = session.query(Comment)
        assert all_comments.count() == expected_result
        assert new_comment.text == text
