from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import Course, Category, Schedule, Student, RegistrationRequest, CourseRequest
from .forms import CourseForm, CategoryForm, ScheduleForm
from .mixins import RedirectToPreviousPageMixin, PaginatorMixin, CheckUserIsTeacher

User = get_user_model()


class HomeTemplateView(ListView):
    model = Category
    template_name = 'home.html'


class CourseListView(PaginatorMixin, ListView):
    model = Course
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category').prefetch_related('schedule_set')


class CourseByCategoryListView(PaginatorMixin, ListView):
    model = Course
    template_name = 'onlineschool/courses_by_category.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context


class CourseDetailView(DetailView):
    model = Course
    slug_url_kwarg = 'course_slug'

    def get_queryset(self):
        return Course.objects.prefetch_related('schedule_set', 'teachers__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user
        course = self.object
        group = course.schedule_set.first()

        registration_request_exists = None
        course_request_exists = None

        if current_user.is_authenticated:
            registration_request_exists = RegistrationRequest.objects\
                .filter(user=current_user, course=group).select_related('user', 'course').exists()
            course_request_exists = CourseRequest.objects \
                .filter(user=current_user, course=course).select_related('user', 'course').exists()

        context['group'] = group
        context['registration_request_exists'] = registration_request_exists
        context['course_request_exists'] = course_request_exists

        # user_already_registered = [
        #     registration_request for registration_request in all_registration_requests
        #     if registration_request.user == current_user
        # ]
        # print('-' * 50)
        # print(user_already_registered)
        # for group in groups:
        #     print(group)
        # print('-' * 50)
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


class ScheduleListView(CheckUserIsTeacher, PaginatorMixin, ListView):
    model = Schedule
    paginate_by = 8


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


class SearchCourseListView(PaginatorMixin, ListView):
    model = Course
    template_name = 'search_course.html'
    paginate_by = 8

    def get_queryset(self):
        object_list = None
        query = self.request.GET.get('keyword')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        return object_list


class StudentCoursesListView(ListView):
    model = Schedule
    template_name = 'onlineschool/student_courses.html'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return Schedule.objects.filter(students=student)


class RegistrationRequestListView(ListView):
    model = RegistrationRequest


def register_registration_request(request, schedule_slug):
    current_user = request.user
    course = get_object_or_404(Schedule, slug=schedule_slug)

    if current_user.is_authenticated:
        request_exists = RegistrationRequest.objects.filter(user=current_user, course=course).exists()
        if request_exists:
            messages.error(request, 'Вы уже подавали заявку на этот курс!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        email = current_user.email
    else:
        current_user = None
        email = request.POST.get('email')

    data = RegistrationRequest.objects.create(
        user=current_user,
        email=email,
        course=course
    )
    data.save()

    messages.success(request, 'Заявка на запись подана!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def register_course_request(request, course_slug):
    current_user = request.user
    course = get_object_or_404(Course, slug=course_slug)

    if current_user.is_authenticated:
        request_exists = CourseRequest.objects.filter(user=current_user, course=course).exists()
        if request_exists:
            messages.error(request, 'Вы уже подавали заявку на этот курс!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        email = current_user.email
    else:
        current_user = None
        email = request.POST.get('email')

    data = CourseRequest.objects.create(
        user=current_user,
        email=email,
        course=course
    )
    data.save()

    messages.success(request, 'Заявка подана! Мы вам сообщим о старте курса.')
    return redirect(request.META.get('HTTP_REFERER', '/'))
