from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=CustomAuthenticationForm,
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', views.SignupPageView.as_view(), name='signup'),
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='reset_password.html',
            success_url=reverse_lazy('accounts:password_reset_done'),
            email_template_name='password_reset_email.html',
        ),
        name='reset_password',
    ),
    path(
        'reset-password-sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_form.html',
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset-password-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
        name='password_reset_complete',
    ),
]
