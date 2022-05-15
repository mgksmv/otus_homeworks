from flask import url_for


def test_home_page(client):
    response = client.get(url_for('accounts_app.login'))
    assert b'Login' in response.data
