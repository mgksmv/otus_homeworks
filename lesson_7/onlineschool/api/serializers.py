from rest_framework.serializers import ModelSerializer

from ..models import Course, Schedule, Category, Teacher, Student, RegistrationRequest, CourseRequest


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class RegistrationRequestSerializer(ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = '__all__'


class CourseRequestSerializer(ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = '__all__'


class StudentCoursesSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
