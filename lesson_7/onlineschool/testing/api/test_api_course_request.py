from datetime import datetime
import pytest

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from onlineschool.models import Student, CourseRequest
from onlineschool.testing.conftest import user, user_teacher, user_student, token_teacher, token_student, course

PATH = '/api/v1/course-request/'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_course_request_list_unauthorized(self, client):
        response = client.get(PATH)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_course_request_list_authorized_teacher_empty(self, user_teacher, token_teacher):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_teacher.key)
        response = api_client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert response.data == []

    def test_course_request_list_authorized_teacher(self, user_teacher, user_student, token_teacher, course):
        student = Student.objects.get(user=user_student)
        CourseRequest.objects.create(
            student=student,
            email=user_student.email,
            course=course,
        )
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_teacher.key)
        response = api_client.get(PATH)

        print(response.data)

        assert response.status_code == HTTP_200_OK
        assert response.data == [
            {
                'id': 1,
                'email': user_student.email,
                'date_created': datetime.today().strftime('%Y-%m-%d'),
                'student': student.id,
                'course': course.id
            }
        ]

    def test_course_request_list_authorized_student(self, user_student, token_student):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_student.key)
        response = api_client.get(PATH)

        assert response.status_code == HTTP_403_FORBIDDEN
