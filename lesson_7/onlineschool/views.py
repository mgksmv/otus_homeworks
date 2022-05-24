from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Course, Category, Schedule
from .forms import CourseForm, CategoryForm, ScheduleForm
from .mixins import RedirectToPreviousPageMixin, PaginatorMixin, CheckUserIsTeacher


class HomeTemplateView(ListView):
    model = Category
    template_name = 'home.html'


class CourseListView(PaginatorMixin, ListView):
    model = Course
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule_objects'] = Schedule.objects.all()
        return context


class CourseByCategoryListView(PaginatorMixin, ListView):
    template_name = 'onlineschool/courses_by_category.html'
    paginate_by = 8

    def get_queryset(self):
        return Course.objects.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context


class CourseDetailView(DetailView):
    model = Course
    slug_url_kwarg = 'course_slug'


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
        print(query)
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        return object_list
