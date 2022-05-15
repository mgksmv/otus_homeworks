from pytest import fixture

from lesson_4.blog_project.config import app


@fixture
def client():
    app.config.update(
        SERVER_NAME='testapp',
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://test:test@localhost:5433/test-blog'
    )
    with app.test_client() as client:
        with app.app_context():
            yield client
