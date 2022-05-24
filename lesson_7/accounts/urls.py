from django.urls import path
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
]
