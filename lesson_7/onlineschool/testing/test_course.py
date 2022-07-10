import pytest

from onlineschool.models import Course, Category, Teacher


@pytest.fixture()
def create_course(db, user):
    category = Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
    teacher = Teacher.objects.get(user=user)
    course = Course.objects.create(
        category=category,
        name='Fullstack разработчик',
        duration=6,
        description='Fullstack разработчик на Python + Vue.js',
        required_knowledge='Базовые знания Python, HTML, CSS',
        after_course='После курса вы будете работать в Google (но это не точно)',
        price=50000,
        slug='fullstack-razrabotchik',
    )
    course.teachers.set([teacher])
    return course


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_create_course_page(self, client, login_user):
        response = client.get('/courses/create-course/')

        assert response.status_code == 200

    def test_create_course_page_unauthenticated(self, client):
        response = client.get('/courses/create-course/')

        assert response.status_code == 302

    def test_create_course(self, client, user, login_user):
        category = Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
        teacher = Teacher.objects.get(user=user)
        response = client.post('/courses/create-course/', {
            'category': category.id,
            'name': 'Fullstack разработчик',
            'duration': 6,
            'teachers': [teacher.id],
            'description': 'Fullstack разработчик на Python + Vue.js',
            'required_knowledge': 'Базовые знания Python, HTML, CSS',
            'after_course': 'После курса вы будете работать в Google (но это не точно)',
            'price': 50000,
            'slug': 'fullstack-razrabotchik',
        })

        assert response.status_code == 302
        assert Course.objects.get(slug='fullstack-razrabotchik').name == 'Fullstack разработчик'
        assert Course.objects.all().count() == 1

    def test_update_course(self, client, user, login_user, create_course):
        response = client.post('/courses/update-course/fullstack-razrabotchik/', {
            'category': create_course.category.id,
            'name': 'Fullstack разработчик 2.0',
            'duration': create_course.duration,
            'teachers': [teacher.id for teacher in create_course.teachers.all()],
            'description': 'Теперь программа курса стала насыщеннее...',
            'required_knowledge': create_course.required_knowledge,
            'after_course': 'Теперь после курса вы будете не только в Google, но ещё и в Microsoft на ночной смене!',
            'price': 100000,
            'slug': 'fullstack-razrabotchik',
        })

        assert response.status_code == 302
        assert Course.objects.get(slug='fullstack-razrabotchik').name == 'Fullstack разработчик 2.0'
        assert Course.objects.all().count() == 1

    def test_course_list_view(self, client, create_course):
        response = client.get('/courses/')

        assert response.status_code == 200
        assert 'Все курсы'.encode('utf-8') in response.content
        assert 'Fullstack разработчик'.encode('utf-8') in response.content

    def test_course_detail_view(self, client, user, create_course):
        response = client.get('/courses/fullstack-razrabotchik/')

        assert response.status_code == 200
        assert 'Fullstack разработчик'.encode('utf-8') in response.content

    def test_course_does_not_exist(self, client):
        response = client.get('/courses/reverse-engineering/')

        assert response.status_code == 404
