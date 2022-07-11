from datetime import datetime

from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.db.models import Prefetch
from rest_framework.authtoken.models import Token

from ..models import Category, Course, Schedule
from ..forms import ContactForm
from ..tasks import send_mail_task
from ..utils import EventCalendar


class HomeTemplateView(ListView):
    model = Category
    template_name = 'home.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('course_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.now()
        cal = EventCalendar(current_date.year, current_date.month, current_date.day)
        html_cal = cal.formatmonth(withyear=True)

        context['calendar'] = mark_safe(html_cal)

        return context


class SearchCourseListView(ListView):
    model = Course
    template_name = 'search_course.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('keyword')
        if query:
            object_list = self.model.objects \
                .select_related('category') \
                .prefetch_related(
                    Prefetch('schedule_set',
                         queryset=Schedule.objects.all().only('course_id', 'start_date', 'is_announced_later'))) \
                .defer('short_description', 'description', 'required_knowledge', 'after_course', 'price',
                       'category__slug') \
                .filter(name__icontains=query)
            return object_list
        return []


class Contact(FormView):
    form_class = ContactForm
    template_name = 'contact_form.html'
    success_url = reverse_lazy('contact')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        current_user = self.request.user
        if current_user.is_authenticated:
            form.fields['email'].initial = current_user.email
            if current_user.first_name and current_user.last_name:
                form.fields['name'].initial = f'{current_user.first_name} {current_user.last_name}'
        return form

    def form_valid(self, form):
        email = form.cleaned_data['email']
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']

        send_mail_task.delay(
            'Сообщение отправлено',
            f'Мы приняли Ваше сообщение. Попытаемся ответить на него как можно скорее!',
            email,
        )
        send_mail_task.delay(
            'Обратная связь',
            f'От: {name} {email}\n'
            f'Сообщение: \n'
            f'{message}',
        )

        messages.success(self.request, 'Сообщение отправлено!')
        return super().form_valid(form)


class APITemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'api.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['token'] = Token.objects.filter(user=request.user).first()
        return self.render_to_response(context)


def generate_token(request):
    User = get_user_model()
    try:
        user = User.objects.get(id=request.user.id)
        token = Token.objects.filter(user=user).first()
        if not token:
            Token.objects.create(user=user)
        else:
            token.delete()
            Token.objects.create(user=user)
        return redirect('api_token')
    except User.DoesNotExist:
        raise Http404
