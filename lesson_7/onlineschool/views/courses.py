from django.db.models import Prefetch
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model

from ..models import Course, Category, Schedule, Student, RegistrationRequest, CourseRequest, Teacher
from ..forms import CourseForm, CategoryForm, ScheduleForm
from ..mixins import RedirectToPreviousPageMixin, CheckUserIsTeacher, CheckUserIsStudent

User = get_user_model()


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
