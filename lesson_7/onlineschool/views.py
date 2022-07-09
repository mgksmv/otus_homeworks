import calendar
from datetime import datetime, timedelta

from django.db.models import Prefetch
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render, Http404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import Token

from .models import Course, Category, Schedule, Student, RegistrationRequest, CourseRequest, Teacher
from .forms import CourseForm, CategoryForm, ScheduleForm, ContactForm
from .mixins import RedirectToPreviousPageMixin, CheckUserIsTeacher, CheckUserIsStudent

from .tasks import send_mail_task
from .utils import EventCalendar
from .forms import DateForm
from config.celery import onlineschool_app

User = get_user_model()


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


class CourseListView(ListView):
    model = Course
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset \
            .select_related('category') \
            .prefetch_related(
                Prefetch('schedule_set',
                     queryset=Schedule.objects.all().only('course_id', 'start_date', 'is_announced_later'))) \
            .defer('short_description', 'description', 'required_knowledge', 'after_course', 'price', 'category__slug')


class CourseByCategoryListView(ListView):
    model = Course
    template_name = 'onlineschool/courses_by_category.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset \
            .select_related('category') \
            .prefetch_related(
                Prefetch('schedule_set',
                     queryset=Schedule.objects.all().only('course_id', 'start_date', 'is_announced_later'))) \
            .defer('short_description', 'description', 'required_knowledge', 'after_course', 'price', 'category__slug') \
            .filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context


class CourseDetailView(DetailView):
    model = Course
    slug_url_kwarg = 'course_slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            Prefetch('schedule_set',
                     queryset=Schedule.objects.all().only('course_id', 'start_date', 'is_announced_later')),
            Prefetch('teachers', queryset=Teacher.objects.all().only('user', 'bio')), 'teachers__user'
        ).defer('category_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user
        course = self.object
        group = course.schedule_set.first()

        registration_request_exists = None
        course_request_exists = None
        user_in_group = None

        if current_user.is_authenticated:
            student = Student.objects.filter(user=current_user).first()
            if student:
                registration_request_exists = RegistrationRequest.objects \
                    .filter(student=student, course=course).select_related('student', 'course').exists()
                course_request_exists = CourseRequest.objects \
                    .filter(student=student, course=course).select_related('student', 'course').exists()
                user_in_group = student in group.students.all()

        context['group'] = group
        context['registration_request_exists'] = registration_request_exists
        context['course_request_exists'] = course_request_exists
        context['user_in_group'] = user_in_group

        return context


class CourseCreateView(CheckUserIsTeacher, RedirectToPreviousPageMixin, CreateView):
    model = Course
    form_class = CourseForm


class CourseUpdateView(CheckUserIsTeacher, RedirectToPreviousPageMixin, UpdateView):
    model = Course
    form_class = CourseForm
    slug_url_kwarg = 'course_slug'
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Курс успешно обновлен!')
        return super().form_valid(form)


class CourseDeleteView(CheckUserIsTeacher, DeleteView):
    model = Course
    slug_url_kwarg = 'course_slug'
    success_url = reverse_lazy('onlineschool:courses')

    def form_valid(self, form):
        messages.success(self.request, 'Курс удалён.')
        return redirect(self.get_success_url())


class CategoryCreateView(CheckUserIsTeacher, RedirectToPreviousPageMixin, CreateView):
    model = Category
    form_class = CategoryForm


class CategoryUpdateView(CheckUserIsTeacher, UpdateView):
    model = Category
    form_class = CategoryForm
    slug_url_kwarg = 'category_slug'
    success_url = reverse_lazy('home')
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Категория успешно обновлена!')
        return super().form_valid(form)


class CategoryDeleteView(CheckUserIsTeacher, DeleteView):
    model = Category
    slug_url_kwarg = 'category_slug'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Категория удалена.')
        return redirect(self.get_success_url())


class ScheduleListView(CheckUserIsTeacher, ListView):
    model = Schedule
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('course').prefetch_related(
            Prefetch('students', queryset=Student.objects.select_related('user').only('user__first_name', 'user__last_name'))
        ) \
            .defer(
            'course__short_description', 'course__description', 'course__required_knowledge', 'course__after_course',
            'course__price', 'course__category_id'
        )


class GroupCreateView(CheckUserIsTeacher, RedirectToPreviousPageMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        course_id = self.request.GET.get('create')
        if course_id:
            form.fields['course'].initial = course_id
        return form


class GroupUpdateView(CheckUserIsTeacher, RedirectToPreviousPageMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    slug_url_kwarg = 'group_slug'
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Группа успешно обновлена!')
        return super().form_valid(form)


class GroupDeleteView(CheckUserIsTeacher, DeleteView):
    model = Schedule
    slug_url_kwarg = 'group_slug'
    success_url = reverse_lazy('onlineschool:schedule')

    def form_valid(self, form):
        messages.success(self.request, 'Группа удалена.')
        return redirect(self.get_success_url())


class SearchCourseListView(ListView):
    model = Course
    template_name = 'search_course.html'
    paginate_by = 8

    def get_queryset(self):
        object_list = None
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


class StudentCoursesListView(CheckUserIsStudent, ListView):
    model = Schedule
    template_name = 'onlineschool/student_courses.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        student = Student.objects.get(user=self.request.user)
        return queryset.select_related('course').prefetch_related(
            Prefetch('students', queryset=Student.objects.select_related('user').only('user__first_name', 'user__last_name'))
        ) \
            .defer('course__short_description', 'course__description', 'course__required_knowledge',
                   'course__after_course', 'course__price', 'course__category_id') \
            .filter(students=student)


class RegistrationRequestListView(CheckUserIsTeacher, ListView):
    model = RegistrationRequest
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('course', 'student', 'student__user') \
            .only(
            'email', 'student', 'student__user__first_name', 'student__user__last_name', 'date_created',
            'course', 'course__name', 'course__slug'
        )


class RegistrationRequestDeleteView(DeleteView):
    model = RegistrationRequest
    success_url = reverse_lazy('onlineschool:registration_requests')

    def form_valid(self, form):
        messages.success(self.request, 'Заявка удалена.')
        return redirect(self.get_success_url())


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


def add_student_to_group(request, course_slug, user_id):
    if not request.user.is_authenticated or request.user.user_type == '2':
        raise PermissionDenied

    course = get_object_or_404(Course, slug=course_slug)
    groups = course.schedule_set.all()
    user = User.objects.filter(id=user_id).only('first_name', 'last_name', 'email').first()
    student = Student.objects.filter(user__id=user_id).first()

    if request.method == 'POST':
        group_id = request.POST.get('group')
        group_to_add_user = Schedule.objects.filter(id=group_id).first()
        group_to_add_user.students.add(student)
        group_to_add_user.save()

        registration_request = RegistrationRequest.objects.filter(student=student, course=course).first()
        registration_request.delete()

        messages.success(request, 'Пользователь добавлен в группу!')
        return redirect('onlineschool:registration_requests')

    return render(request, 'onlineschool/add_user_to_group.html', context={'groups': groups, 'user': user})


def register_registration_request(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    current_user = request.user

    if current_user.is_authenticated:
        if current_user.user_type == '1':
            messages.error(
                request, 'Для регистрации вы должны быть студентом :) Зарегистрируйте аккаунт студента для записи.'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

        student = Student.objects.filter(user=current_user).first()
        request_exists = RegistrationRequest.objects.filter(student=student, course=course).exists()
        if request_exists:
            messages.error(request, 'Вы уже подавали заявку на этот курс!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        email = current_user.email
    else:
        student = None
        email = request.POST.get('email')
        account_exists = User.objects.filter(email=email).first()
        if account_exists:
            messages.error(
                request,
                f'У Вас имеется аккаунт, зарегистрированный на почту {email}! Войдите и подайте заявку с аккаунта.'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

    data = RegistrationRequest.objects.create(
        student=student,
        email=email,
        course=course
    )
    data.save()

    send_mail_task.delay(
        'Заявка на запись подана!',
        f'Заявка на запись на курс {course.name} успешно подана. Мы Вам сообщим, когда начнётся курс.',
        email,
    )
    send_mail_task.delay(
        'Новая заявка',
        f'Подана новая заявка на курс {course.name} от {student if student else email}\n'
        f'Посмотреть все заявки: {request.get_host() + reverse("onlineschool:registration_requests")}'
    )

    messages.success(request, 'Заявка на запись подана!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register_course_request(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    current_user = request.user

    if current_user.is_authenticated:
        if current_user.user_type == '1':
            messages.error(
                request, 'Для подачи заявки вы должны быть студентом :)'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

        student = Student.objects.filter(user=current_user).first()
        request_exists = CourseRequest.objects.filter(student=student, course=course).exists()
        if request_exists:
            messages.error(request, 'Вы уже подавали заявку на этот курс!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        email = current_user.email
    else:
        student = None
        email = request.POST.get('email')
        account_exists = User.objects.filter(email=email).first()
        if account_exists:
            messages.error(
                request,
                f'У Вас имеется аккаунт, зарегистрированный на почту {email}! Войдите и подайте заявку с аккаунта.'
            )
            return redirect(request.META.get('HTTP_REFERER', '/'))

    data = CourseRequest.objects.create(
        student=student,
        email=email,
        course=course
    )
    data.save()

    send_mail_task.delay(
        'Заявка на старт курса подана!',
        f'Заявка на старт курса {course.name} успешно подана. Мы Вам сообщим, когда начнётся набор в группу.',
        email,
    )
    send_mail_task.delay(
        'Новая заявка',
        f'Подана новая заявка на курс {course.name} от {student if student else email}\n'
        f'Группы на курс ещё нет, начать набор? '
        f'{request.get_host() + reverse("onlineschool:create_group") + "?create=" + str(course.id)}'
    )

    messages.success(request, 'Заявка подана! Мы вам сообщим о старте курса.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def send_registration_link(request, email, course_slug):
    course = Course.objects.filter(slug=course_slug).first()
    send_mail_task.delay(
        'Online School. Регистрация.',
        f'Вы недавно подавали заявку на запись на курс {course.name}\n'
        f'Чтобы записать Вас в группу, потребуется создать аккаунт в нашем сайте.\n'
        f'Перейдите по ссылке ниже, чтобы создать новый аккаунт:\n'
        f'{request.get_host() + reverse("accounts:signup")}',
        email,
    )

    messages.success(request, 'Ссылка на регистрацию отправлена.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


# Calendar
def get_date(req_day):
    if req_day:
        try:
            year, month, day = (int(x) for x in req_day.split('-'))
            return datetime(year, month, day)
        except ValueError:
            year, month = (int(x) for x in req_day.split('-'))
            return datetime(year, month, day=1)
    return datetime.today()


def prev_month(current_date):
    first = current_date.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'date=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(current_date):
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    last = current_date.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'date=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class ScheduleCalendarView(ListView):
    model = Schedule
    template_name = 'onlineschool/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = get_date(self.request.GET.get('date', None))
        cal = EventCalendar(current_date.year, current_date.month, current_date.day)
        html_cal = cal.formatmonth(withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(current_date)
        context['next_month'] = next_month(current_date)
        context['form'] = DateForm()

        return context
