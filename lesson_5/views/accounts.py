from flask import Blueprint, request, render_template, abort, url_for, redirect, flash, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from lesson_5.forms import SingUpForm, LoginForm, EditUserForm, ResetEmailForm, ResetPasswordForm
from lesson_5.models import db, User, Blog

accounts_app = Blueprint('accounts_app', __name__)
mail = Mail(current_app)


def send_email_thread(msg):
    with current_app.app_context():
        mail.send(msg)


def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    thr = Thread(target=send_email_thread, args=[msg])
    thr.start()


def send_password_reset_link(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    password_reset_url = url_for(
        'accounts_app.token_reset',
        token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True
    )

    html = render_template(
        'accounts/email_reset.html',
        password_reset_url=password_reset_url)

    send_email('Password Reset Requested', [user_email], html)


@accounts_app.route('/reset/', methods=['GET', 'POST'])
def reset_email():
    form = ResetEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()
        if not user:
            flash('Invalid email address!', category='danger')
            return render_template('accounts/password_reset.html', form=form)
        else:
            send_password_reset_link(user.email)
            flash('Please check your email for a password reset link.', category='info')
        return redirect(url_for('accounts_app.login'))

    return render_template('accounts/password_reset.html', form=form)


@accounts_app.route('/reset/<token>', methods=['GET', 'POST'])
def token_reset(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', category='danger')
        return redirect(url_for('accounts_app.login'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', category='danger')
            return redirect(url_for('accounts_app.login'))

        new_password = form.password.data
        hash_and_salted_password = generate_password_hash(
            new_password,
            method='pbkdf2:sha256',
            salt_length=8,
        )
        user.password = hash_and_salted_password
        db.session.add(user)
        db.session.commit()

        logout_user()

        flash('Your password has been updated!', category='info')
        return redirect(url_for('accounts_app.login'))

    return render_template('accounts/reset_token_pass.html', token=token, form=form)


@accounts_app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SingUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data

            user_by_username_exist = User.query.filter_by(username=username).one_or_none()
            user_by_email_exist = User.query.filter_by(email=email).one_or_none()

            if user_by_username_exist and user_by_email_exist:
                flash('This username is already taken. Try something else.', category='danger')
                flash('User with this email already exist. Try something else.', category='danger')
                return redirect(url_for('accounts_app.signup'))
            elif user_by_username_exist:
                flash('This username is already taken. Try something else.', category='danger')
                return redirect(url_for('accounts_app.signup'))
            elif user_by_email_exist:
                flash('User with this email already exist. Try something else.', category='danger')
                return redirect(url_for('accounts_app.signup'))
            else:
                password_1 = form.password_1.data
                password_2 = form.password_2.data
                if password_1 != password_2:
                    flash('Passwords do not match! Try again', category='danger')
                    return redirect(url_for('accounts_app.signup'))
                else:
                    hash_and_salted_password = generate_password_hash(
                        password_1,
                        method='pbkdf2:sha256',
                        salt_length=8,
                    )
                    new_user = User(
                        username=username,
                        email=email,
                        password=hash_and_salted_password,
                    )
                    db.session.add(new_user)
                    db.session.commit()

                    flash('Your account has been successfully created! Login to continue.', category='info')

                    return redirect(url_for('accounts_app.login'))

    return render_template('accounts/signup.html', form=form)


@accounts_app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accounts_app.get_user_profile', user_id=current_user.id))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).one_or_none()

            if not user:
                flash('This username does not exist, please try again.', category='danger')
                return redirect(url_for('accounts_app.login'))
            elif not check_password_hash(user.password, password):
                flash('Password is incorrect, please try again.', category='danger')
                return redirect(url_for('accounts_app.login'))
            else:
                if request.form.get('checkbox'):
                    login_user(user, remember=True)
                else:
                    login_user(user)
                flash('You successfully logged in!', category='info')
                return redirect(url_for('main_app.home'))

    return render_template('accounts/login.html', form=form)


@accounts_app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('accounts_app.login'))


@accounts_app.route('/user/<int:user_id>/')
@login_required
def get_user_profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    user_blogs = Blog.query.filter_by(user_id=user_id).order_by(Blog.id.desc()).paginate(per_page=10)
    return render_template('accounts/user_profile.html', user=user, user_blogs=user_blogs)


@accounts_app.route('/user/<int:user_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_user_profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = EditUserForm()

    if current_user.id == user_id:
        if request.method == 'GET':
            form.bio.data = user.bio
        if request.method == 'POST':
            if form.validate_on_submit():
                username = form.username.data
                first_name = form.first_name.data
                last_name = form.last_name.data
                bio = form.bio.data
                email = form.email.data
                password = form.password.data

                if password:
                    hash_and_salted_password = generate_password_hash(
                        password,
                        method='pbkdf2:sha256',
                        salt_length=8,
                    )
                    user.password = hash_and_salted_password

                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.bio = bio
                user.email = email
                db.session.commit()

                flash('Your profile has been updated!', category='info')
                return redirect(url_for('accounts_app.get_user_profile', user_id=user_id))
            else:
                print(form.errors)

        return render_template('accounts/edit_user_profile.html', user=user, form=form)

    else:
        abort(404)
