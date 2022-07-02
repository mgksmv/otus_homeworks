import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user(db):
    return User.objects.create_superuser(email='test@test.com', password='test12345')


@pytest.fixture()
def login_user(db, user, client):
    return client.login(email='test@test.com', password='test12345')


@pytest.fixture()
def user_teacher(db):
    return User.objects.create(
        email='teacher@test.com',
        first_name='Test',
        last_name='Teacher',
        password='teacher12345',
        user_type='1',
    )


@pytest.fixture()
def user_student(db):
    return User.objects.create(
        email='student@test.com',
        first_name='Test',
        last_name='Student',
        password='student12345',
        user_type='2',
    )
