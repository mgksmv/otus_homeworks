import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_superuser(user):
    get_user = User.objects.get(email='test@test.com')
    assert get_user.is_superuser
    assert get_user.id == 1


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
def test_course_list_view(client):
    response = client.get('/courses/')
    text = 'Все курсы'.encode('utf-8')
    assert response.status_code == 200
    assert text in response.content


@pytest.mark.django_db
def test_forbidden_page(client, login_user):
    response = client.get('/courses/my-courses/')
    assert response.status_code == 403
