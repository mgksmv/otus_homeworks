import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user(db):
    return User.objects.create_superuser(email='test@test.com', password='test12345')


@pytest.mark.django_db
def test_my_user(user):
    me = User.objects.get(email='test@test.com')
    assert me.is_superuser
    assert me.id == 1


@pytest.mark.django_db
def test_user_count(user):
    all_users = User.objects.all()
    assert all_users.count() == 1


@pytest.mark.django_db
def test_home_page(client):
    response = client.get('/')
    text = 'Добро пожаловать'.encode('utf-8')
    assert response.status_code == 200
    assert text in response.content


@pytest.mark.django_db
def test_forbidden_page(client, user):
    client.login(email='test@test.com', password='test12345')
    response = client.get('/courses/my-courses/')
    assert response.status_code == 403
