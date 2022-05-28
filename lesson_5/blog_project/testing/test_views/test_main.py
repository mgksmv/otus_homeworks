from flask import url_for, current_app
from flask_login import current_user

try:
    from lesson_5.blog_project.models import User
except ImportError:
    from blog_project.models import User


def test_home_page(client):
    response = client.get(url_for('main_app.home'))
    assert response.status_code == 302


def test_home_page_with_user(client):
    with client.session_transaction() as session:
        new_user = User(
            username='testuser',
            email='test@test.com',
            password='password'
        )
        session['user'] = new_user
        response = client.post(
            '/login/', data={'username': session['user'].username, 'password': session['user'].password}
        )

    assert response.status_code == 200
    assert session['user'].username == 'testuser'
    # new_response = client.get(url_for('main_app.home'))
    # assert b'All blogs' in new_response.data
