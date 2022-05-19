from flask import url_for
from flask_login import login_user


def test_home_page(client):
    response = client.get(url_for('main_app.home'))
    assert response.status_code == 302


def test_home_page_with_user(client, user):
    response = client.post('/login/', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200
    new_response = client.get(url_for('main_app.home'))
    assert b'All blogs' in new_response.data
