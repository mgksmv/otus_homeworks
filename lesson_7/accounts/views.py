from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import CustomUserCreationForm


class SignupPageView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated != True

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'signup.html'
