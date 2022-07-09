import pytest

from ..models import Category


@pytest.mark.django_db
class Tests:
    def test_create_category_page(self, client, login_user):
        response = client.get('/courses/create-category/')
        assert response.status_code == 200

    def test_create_category_page_unauthenticated(self, client):
        response = client.get('/courses/create-category/')
        assert response.status_code == 302

    @pytest.mark.parametrize('name, color, slug', [
        ('Web Development', '#0e72ed', 'web-development'),
        ('Reverse Engineering', '#edbc0e', 'reverse-engineering'),
        ('QA', '#ed0e0e', 'qa'),
    ])
    def test_create_category_and_if_category_in_home_page(self, client, login_user, name, color, slug):
        response = client.post('/courses/create-category/', {
            'name': name,
            'color': color,
            'slug': slug,
        })
        created_category = Category.objects.get(slug=slug)
        assert response.status_code == 302
        assert Category.objects.all().count() == 1
        assert created_category.name == name
        assert created_category.color == color
        assert created_category.slug == slug

        response = client.get('/')
        assert name.encode('utf-8') in response.content

    def test_update_category(self, client, login_user, user):
        Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
        response = client.post('/courses/update-category/web-development/', {
            'name': 'Web dev and testing',
            'color': '#0e72ed',
            'slug': 'web-development',
        })
        assert response.status_code == 302
        assert Category.objects.get(slug='web-development').name == 'Web dev and testing'

    def test_course_by_category(self, client):
        Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
        response = client.get('/courses/category/web-development/')
        assert response.status_code == 200

    def test_course_by_category_does_not_exist(self, client):
        response = client.get('/courses/category/web-development/')
        assert response.status_code == 404
