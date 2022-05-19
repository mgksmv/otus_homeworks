import click
from flask_login import LoginManager, current_user
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash

from lesson_5 import app
from lesson_5.models import db, User
from lesson_5.views import accounts_app, blogs_app, main_app


def create_app():
    app.register_blueprint(accounts_app)
    app.register_blueprint(blogs_app)
    app.register_blueprint(main_app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'accounts_app.login'
    login_manager.login_message_category = 'danger'

    CKEditor(app)
    Bcrypt(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def base():
        return dict(user=current_user)

    return app


@app.cli.command('createsuperuser', help='Create a super user.')
@click.option('--username')
@click.option('--email')
@click.option('--password')
def create_super_user(username, email, password):
    print('Creating a super user...')
    hash_and_salted_password = generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=8,
    )
    new_user = User(username=username, email=email, password=hash_and_salted_password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()
    print('Done!')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
