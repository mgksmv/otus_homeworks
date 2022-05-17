from django.contrib import admin
from django.utils.html import format_html

from .models import Teacher, Student, Review, Course, Schedule


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    @staticmethod
    def thumbnail(obj: Teacher):
        return format_html(f'<img src="{obj.photo.url}" width="100" />')

    @staticmethod
    def shorten_bio(obj: Teacher):
        if len(obj.bio) < 40:
            return obj.bio
        return f'{obj.bio[:36]}...'

    @staticmethod
    def full_name(obj):
        return str(obj)

    thumbnail.short_description = 'Фото'
    shorten_bio.short_description = 'Биография'
    full_name.short_description = 'ФИО'

    list_display = ['thumbnail', 'full_name', 'short_bio', 'shorten_bio']
    list_display_links = ['full_name']
    search_fields = ['first_name', 'last_name', 'short_bio', 'bio']

    class Meta:
        model = Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    @staticmethod
    def thumbnail(obj: Student):
        return format_html(f'<img src="{obj.photo.url}" width="100" />')

    @staticmethod
    def full_name(obj):
        return str(obj)

    thumbnail.short_description = 'Фото'
    full_name.short_description = 'ФИО'

    list_display = ['thumbnail', 'full_name', 'birthday', 'email', 'phone']
    list_display_links = ['full_name']
    search_fields = ['full_name', 'birthday', 'email', 'phone']

    class Meta:
        model = Student


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'rating', 'text']
    list_display_links = ['student']
    search_fields = ['student', 'rating', 'text']

    class Meta:
        model = Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    @staticmethod
    def shorten_description(obj: Course):
        if len(obj.description) < 40:
            return obj.description
        return f'{obj.description[:36]}...'

    shorten_description.short_description = 'Описание'

    list_display = ['name', 'duration', 'shorten_description']
    list_display_links = ['name']
    search_fields = ['name', 'duration', 'shorten_description']
    filter_horizontal = ['teachers', 'reviews']

    class Meta:
        model = Course


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['course', 'start_date', 'end_date']
    list_display_links = ['course']
    search_fields = ['course', 'start_date', 'end_date']
    filter_horizontal = ['students']

    class Meta:
        model = Schedule
