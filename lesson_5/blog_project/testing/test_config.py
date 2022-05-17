from pytest import fixture

from lesson_5.blog_project.app import create_app
from lesson_5.blog_project.models import db, User
from lesson_5.blog_project.views import accounts_app, blogs_app, main_app


@fixture
def client():
    app = create_app()
    app.config.update(
        SERVER_NAME='testapp',
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://test:test@localhost:5433/testblog'
    )
    app.register_blueprint(accounts_app, name='test_accounts')
    app.register_blueprint(blogs_app, name='test_blogs')
    app.register_blueprint(main_app, name='test_main')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@fixture
def user():
    new_user = User(
        username='testuser',
        email='test@test.com',
        password='password'
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user
