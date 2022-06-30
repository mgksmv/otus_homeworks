from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'course', views.CourseViewSet)
router.register(r'schedule', views.ScheduleViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'teacher', views.TeacherViewSet)
router.register(r'student', views.StudentViewSet)
router.register(r'registration-request', views.RegistrationRequestViewSet)
router.register(r'course-request', views.CourseRequestViewSet)
router.register(r'student-courses', views.StudentCoursesViewSet, basename='student_courses')

app_name = 'onlineschool_api'

urlpatterns = router.urls
