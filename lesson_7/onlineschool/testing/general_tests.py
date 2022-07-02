import pytest
from django.contrib.auth import get_user_model

from .test_course import create_course

User = get_user_model()


@pytest.mark.django_db
class Tests:
    def test_superuser(self, user):
        get_user = User.objects.get(email='test@test.com')
        assert get_user.is_superuser
        assert get_user.id == 1

    def test_user_count(self, user):
        all_users = User.objects.all()
        assert all_users.count() == 1

    def test_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert 'Добро пожаловать'.encode('utf-8') in response.content

    def test_contact_page(self, client):
        response = client.get('/contact/')
        assert response.status_code == 200
        assert 'Связь с нами'.encode('utf-8') in response.content

    def test_search_nonexistent_course(self, client):
        response = client.get('/courses/search/?keyword=asdasdasd')
        assert response.status_code == 200
        assert 'Ничего не найдено'.encode('utf-8') in response.content

    def test_search_existed_course(self, client, user, create_course):  # create_course is a fixture from test_course.py
        response = client.get('/courses/search/?keyword=fulls')
        assert response.status_code == 200
        assert 'Ничего не найдено'.encode('utf-8') not in response.content
        assert 'Fullstack разработчик'.encode('utf-8') in response.content

    def test_forbidden_page(self, client, login_user):
        response = client.get('/courses/my-courses/')
        assert response.status_code == 403
