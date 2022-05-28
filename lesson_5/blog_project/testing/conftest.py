from pytest import fixture

try:
    from lesson_5.blog_project.app import create_app
    from lesson_5.blog_project.models import db, User
except ImportError:
    from blog_project.app import create_app
    from blog_project.models import db, User


@fixture
def client():
    app = create_app()
    app.config.update(
        SERVER_NAME='testapp',
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://test:test@localhost:5433/testblog',
        PRESERVE_CONTEXT_ON_EXCEPTION=False,
    )
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


# @fixture
# def user():
#     new_user = User(
#         username='testuser',
#         email='test@test.com',
#         password='password'
#     )
#     db.session.add(new_user)
#     db.session.commit()
#     return new_user
