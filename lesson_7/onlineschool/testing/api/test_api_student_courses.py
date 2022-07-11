import pytest

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from onlineschool.testing.conftest import user, user_teacher, user_student, token_teacher, token_student

PATH = '/api/v1/student-courses/'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_student_courses_list_unauthorized(self, client):
        response = client.get(PATH)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_student_courses_list_authorized_teacher(self, user_teacher, token_teacher):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_teacher.key)
        response = api_client.get(PATH)

        assert response.status_code == HTTP_403_FORBIDDEN

    def test_student_courses_list_authorized_student(self, user_student, token_student):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_student.key)
        response = api_client.get(PATH)

        assert response.status_code == HTTP_200_OK
