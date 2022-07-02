from django.contrib.auth.mixins import UserPassesTestMixin


class RedirectToPreviousPageMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        try:
            return self.request.session['previous_page']
        except KeyError:
            return self.request.path_info


class CheckUserIsTeacher(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.user_type == '1'


class CheckUserIsStudent(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.user_type == '2'
