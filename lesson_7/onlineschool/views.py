from django.db.models import Prefetch
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .models import Course, Category, Schedule, Student, RegistrationRequest, CourseRequest, Teacher
from .forms import CourseForm, CategoryForm, ScheduleForm
from .mixins import RedirectToPreviousPageMixin, CheckUserIsTeacher, CheckUserIsStudent

User = get_user_model()


class HomeTemplateView(ListView):
    model = Category
    template_name = 'home.html'


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


class CourseDeleteView(CheckUserIsTeacher, DeleteView):
    model = Course
    slug_url_kwarg = 'course_slug'
    success_url = reverse_lazy('onlineschool:courses')


class CategoryCreateView(CheckUserIsTeacher, RedirectToPreviousPageMixin, CreateView):
    model = Category
    form_class = CategoryForm


class CategoryUpdateView(CheckUserIsTeacher, UpdateView):
    model = Category
    form_class = CategoryForm
    slug_url_kwarg = 'category_slug'
    success_url = reverse_lazy('home')
    template_name_suffix = '_update_form'


class CategoryDeleteView(CheckUserIsTeacher, DeleteView):
    model = Category
    slug_url_kwarg = 'category_slug'
    success_url = reverse_lazy('home')


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


class GroupUpdateView(CheckUserIsTeacher, RedirectToPreviousPageMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    slug_url_kwarg = 'group_slug'
    template_name_suffix = '_update_form'


class GroupDeleteView(CheckUserIsTeacher, DeleteView):
    model = Schedule
    slug_url_kwarg = 'group_slug'
    success_url = reverse_lazy('onlineschool:schedule')


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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('course', 'student', 'student__user') \
            .only(
            'email', 'student', 'student__user__first_name', 'student__user__last_name', 'date_created',
            'course', 'course__name', 'course__slug'
        )


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

    data = RegistrationRequest.objects.create(
        student=student,
        email=email,
        course=course
    )
    data.save()

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

    data = CourseRequest.objects.create(
        student=student,
        email=email,
        course=course
    )
    data.save()

    messages.success(request, 'Заявка подана! Мы вам сообщим о старте курса.')
    return redirect(request.META.get('HTTP_REFERER', '/'))
