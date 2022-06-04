from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import UserPassesTestMixin


class RedirectToPreviousPageMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class CheckUserIsTeacher(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == '1'
