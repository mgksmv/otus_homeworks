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

    def test_signup_user(self, client):
        response = client.post('/accounts/signup/', {
            'email': 'test2@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'birthday': '1999-09-09',
            'phone': 88005553535,
            'user_type': '1',
            'password1': 'test111222333',
            'password2': 'test111222333',
        })
        assert response.status_code == 302
        assert User.objects.all().count() == 1
        assert User.objects.get(email='test2@test.com').first_name == 'Test'
        assert User.objects.get(email='test2@test.com').last_name == 'User'

    def test_login_user(self, client, user):
        response = client.post('/accounts/login/', {
            'username': 'test@test.com',
            'password': 'test12345',
        })
        assert response.status_code == 302

    def test_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert 'Добро пожаловать'.encode('utf-8') in response.content

    def test_contact_page(self, client):
        response = client.get('/contact/')
        assert response.status_code == 200
        assert 'Связь с нами'.encode('utf-8') in response.content

    def test_api_token_page(self, client, login_user):
        response = client.get('/api-token/')
        assert response.status_code == 200
        assert b'/api/v1/' in response.content

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

    def test_forbidden_my_courses_page_for_teacher(self, client, user_teacher):
        client.force_login(user_teacher)
        response = client.get('/courses/my-courses/')
        assert response.status_code == 403

    def test_forbidden_create_course_page_for_student(self, client, user_student):
        client.force_login(user_student)
        response = client.get('/courses/create-course/')
        assert response.status_code == 403

    def test_forbidden_create_category_page_for_student(self, client, user_student):
        client.force_login(user_student)
        response = client.get('/courses/create-category/')
        assert response.status_code == 403

    def test_forbidden_create_group_page_for_student(self, client, user_student):
        client.force_login(user_student)
        response = client.get('/courses/create-group/')
        assert response.status_code == 403

    def test_forbidden_schedule_page_for_student(self, client, user_student):
        client.force_login(user_student)
        response = client.get('/courses/schedule/')
        assert response.status_code == 403

    def test_forbidden_registration_requests_page_for_student(self, client, user_student):
        client.force_login(user_student)
        response = client.get('/courses/registration-requests/')
        assert response.status_code == 403
