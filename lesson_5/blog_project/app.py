import click
from flask import Flask
from flask_login import LoginManager, current_user
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
from decouple import config

try:
    from lesson_5.blog_project.mail import mail
    from lesson_5.blog_project.models import db, User, migrate
    from lesson_5.blog_project.views import accounts_app, blogs_app, main_app
except ImportError:
    from blog_project.mail import mail
    from blog_project.models import db, User, migrate
    from blog_project.views import accounts_app, blogs_app, main_app


def create_app():
    app = Flask(__name__, static_folder='static')

    with app.app_context():
        app.config.update(
            ENV=config('ENV'),
            SECRET_KEY=config('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=config('SQLALCHEMY_DATABASE_URI'),
            MAIL_SERVER=config('MAIL_SERVER'),
            MAIL_PORT=config('MAIL_PORT'),
            MAIL_USE_TLS=config('MAIL_USE_TLS'),
            MAIL_USE_SSL=config('MAIL_USE_SSL'),
            MAIL_USERNAME=config('MAIL_USERNAME'),
            MAIL_PASSWORD=config('MAIL_PASSWORD'),
            MAIL_DEFAULT_SENDER=config('MAIL_DEFAULT_SENDER'),
        )

        app.register_blueprint(accounts_app)
        app.register_blueprint(blogs_app)
        app.register_blueprint(main_app)

        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'accounts_app.login'
        login_manager.login_message_category = 'danger'

        CKEditor(app)
        Bcrypt(app)

        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)

        create_commands(app)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.context_processor
        def base():
            return dict(user=current_user)

    return app


def create_commands(app):
    def validate_username(ctx, param, value):
        if len(value) < 6:
            raise click.BadParameter('Username must contain at least 6 characters!')
        return value

    def validate_email(ctx, param, value):
        if '@' not in value:
            raise click.BadParameter('Email must contain @ symbol!')
        return value

    def validate_password(ctx, param, value):
        if len(value) < 6:
            raise click.BadParameter('Password must contain at least 6 characters!')
        return value

    @app.cli.command('createsuperuser', help='Create a super user.')
    @click.option('--username', callback=validate_username)
    @click.option('--email', callback=validate_email)
    @click.option('--password', callback=validate_password)
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
    application = create_app()
    application.run(debug=True, host='0.0.0.0')