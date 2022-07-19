import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

from onlineschool.models import Category, Schedule, Course, Teacher, Student

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'


class ScheduleType(DjangoObjectType):
    class Meta:
        model = Schedule
        fields = '__all__'


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = '__all__'


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = '__all__'


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_categories = graphene.List(CategoryType)
    all_schedule = graphene.List(ScheduleType)
    all_courses = graphene.List(CourseType)
    all_teachers = graphene.List(TeacherType)
    all_students = graphene.List(StudentType)

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_schedule(self, info):
        return Schedule.objects.all()

    def resolve_all_courses(self, info):
        return Course.objects.all()

    def resolve_all_teachers(self, info):
        return Teacher.objects.all()

    def resolve_all_students(self, info):
        return Student.objects.all()


schema = graphene.Schema(query=Query)
