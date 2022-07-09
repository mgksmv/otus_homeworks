from ..models import RegistrationRequest, CourseRequest, Student
from .test_course import create_course


class Tests:
    def test_registration_request_page_unauthenticated(self, client):
        response = client.get('/courses/registration-requests/')
        assert response.status_code == 302

    def test_registration_request_page_student_authenticated(self, client, user_student):
        client.force_login(user_student)
        response = client.get('/courses/registration-requests/')
        assert response.status_code == 403

    def test_registration_request_page_teacher_authenticated(self, client, user_teacher):
        client.force_login(user_teacher)
        response = client.get('/courses/registration-requests/')
        assert 'Заявки на запись на курс'.encode('utf-8') in response.content
        assert response.status_code == 200

    def test_registration_request_list_view(self, client, user_student, user_teacher, create_course):
        client.force_login(user_teacher)
        student = Student.objects.get(user=user_student)
        RegistrationRequest.objects.create(student=student, email=user_student.email, course=create_course)
        response = client.get('/courses/registration-requests/')
        assert response.status_code == 200
        assert f'{user_student.email}'.encode('utf-8') in response.content

    def test_registration_request(self, client, create_course, user_teacher):
        post_response = client.post(f'/courses/{create_course.slug}/register/', data={'email': 'test@test.com'})
        assert post_response.status_code == 302
        client.force_login(user_teacher)
        response = client.get('/courses/registration-requests/')
        assert response.status_code == 200
        assert 'test@test.com'.encode('utf-8') in response.content

    def test_course_request(self, client, create_course, user_teacher):
        create_course.is_announced_later = True
        create_course.save()
        get_response = client.get(f'/courses/{create_course.slug}/')
        assert get_response.status_code == 200
        assert 'о дате старта будет объявлено позже'.encode('utf-8') in get_response.content
        post_response = client.post(f'/courses/{create_course.slug}/register/', data={'email': 'test@test.com'})
        assert post_response.status_code == 302
