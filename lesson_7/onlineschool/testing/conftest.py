import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user(db):
    return User.objects.create_superuser(email='test@test.com', password='test12345')


@pytest.fixture()
def login_user(db, user, client):
    return client.login(email='test@test.com', password='test12345')
