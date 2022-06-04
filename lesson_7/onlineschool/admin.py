from django.contrib import admin
from django.utils.html import format_html

from .models import Teacher, Student, Review, Course, Schedule, Category, RegistrationRequest, CourseRequest
from .forms import CategoryFormAdmin


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    def thumbnail(self, obj: Teacher):
        return format_html(f'<img src="{obj.user.photo.url}" width="100" />')

    def shorten_bio(self, obj: Teacher):
        if len(obj.bio) < 40:
            return obj.bio
        return f'{obj.bio[:36]}...'

    thumbnail.short_description = 'Фото'
    shorten_bio.short_description = 'Биография'

    list_display = ['thumbnail', 'user']
    list_display_links = ['user']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    def thumbnail(self, obj: Student):
        return format_html(f'<img src="{obj.user.photo.url}" width="100" />')

    thumbnail.short_description = 'Фото'

    list_display = ['thumbnail', 'user']
    list_display_links = ['user']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'rating', 'text']
    list_display_links = ['student']
    search_fields = ['student', 'rating', 'text']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    def shorten_description(self, obj: Course):
        if len(obj.description) < 40:
            return obj.description
        return f'{obj.description[:36]}...'

    shorten_description.short_description = 'Описание'

    list_display = ['name', 'duration', 'shorten_description']
    list_display_links = ['name']
    search_fields = ['name', 'duration', 'shorten_description']
    filter_horizontal = ['teachers']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'end_date']
    list_display_links = ['course']
    search_fields = ['course', 'start_date', 'end_date']
    filter_horizontal = ['students']
    prepopulated_fields = {'slug': ('course',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryFormAdmin
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'student', 'course', 'date_created']
    list_display_links = ['email']
    readonly_fields = ['date_created']


@admin.register(CourseRequest)
class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'student', 'course', 'date_created']
    list_display_links = ['email']
    readonly_fields = ['date_created']
