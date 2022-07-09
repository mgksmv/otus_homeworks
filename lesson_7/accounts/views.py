from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import CustomUserCreationForm
from .tokens import token_generator
from .tasks import send_activation_email
from onlineschool.models import Student, RegistrationRequest
from config.celery import onlineschool_app

User = get_user_model()


class SignupPageView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return not self.request.user.is_authenticated

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'signup.html'

    def form_valid(self, form):
        self.object = form.save()
        account_activation(self.request, self.object)
        return super().form_valid(form)


def account_activation(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Активация аккаунта на Online School'
    message = render_to_string('account_verification_email.html', context={
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })
    send_activation_email.delay(mail_subject, message, user.email)

    url = reverse('accounts:resend_activation_link', kwargs={'email': user.email})
    popup_message = f'''
        Для завершения регистрации активируйте аккаунт с помощью ссылки, которую мы отправили Вам на E-mail {user.email}
        <br>
        Сообщение не пришло? <a href="{url}">Отправить снова</a>
    '''

    messages.success(
        request,
        mark_safe(popup_message),
    )


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        if user.user_type == '2':
            student_instance = Student.objects.get(user=user)
            user_registration_requests = RegistrationRequest.objects.filter(email=user.email).all()
            if user_registration_requests:
                for registration_request in user_registration_requests:
                    registration_request.student = student_instance
                    registration_request.save()

        messages.success(request, 'Ваш аккаунт активирован. Теперь Вы можете войти.')
    else:
        messages.error(request, 'Ссылка недействительна!')

    return redirect('accounts:login')


def resend_activation_link(request, email):
    user = User.objects.get(email=email)
    if not user.is_active:
        account_activation(request, user)
        return redirect('accounts:login')
    return redirect('home')
