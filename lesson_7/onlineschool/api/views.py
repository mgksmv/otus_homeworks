from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from ..models import Course, Schedule, Category, Teacher, Student, RegistrationRequest, CourseRequest
from .serializers import (
    CourseSerializer,
    ScheduleSerializer,
    CategorySerializer,
    TeacherSerializer,
    StudentSerializer,
    RegistrationRequestSerializer,
    CourseRequestSerializer, StudentCoursesSerializer
)
from .permissions import IsTeacherPermission, IsStudentPermission


class CourseViewSet(ModelViewSet):
    queryset = Course.objects
    serializer_class = CourseSerializer

    def get_queryset(self):
        return super().get_queryset() \
            .select_related('category') \
            .prefetch_related('teachers', 'teachers__user')


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return super().get_queryset() \
            .select_related('course') \
            .prefetch_related('students', 'students__user')


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects
    serializer_class = CategorySerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('user')


class StudentViewSet(ModelViewSet):
    queryset = Student.objects
    serializer_class = StudentSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('user').prefetch_related('wishlist')


class RegistrationRequestViewSet(ModelViewSet):
    permission_classes = [IsTeacherPermission]
    queryset = RegistrationRequest.objects
    serializer_class = RegistrationRequestSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'student__user', 'course')


class CourseRequestViewSet(ModelViewSet):
    permission_classes = [IsTeacherPermission]
    queryset = CourseRequest.objects
    serializer_class = CourseRequestSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'student__user', 'course')


class StudentCoursesViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsStudentPermission]
    queryset = Schedule.objects
    serializer_class = StudentCoursesSerializer

    def get_queryset(self):
        return super().get_queryset().filter(students__user=self.request.user)
