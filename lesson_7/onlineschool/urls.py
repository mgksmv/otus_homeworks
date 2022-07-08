from django.urls import path

from . import views

app_name = 'onlineschool'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='courses'),
    path('search/', views.SearchCourseListView.as_view(), name='search'),
    path('schedule/', views.ScheduleListView.as_view(), name='schedule'),
    path('schedule-calendar/', views.ScheduleCalendarView.as_view(), name='schedule_calendar'),
    path('create-course/', views.CourseCreateView.as_view(), name='create_course'),
    path('update-course/<slug:course_slug>/', views.CourseUpdateView.as_view(), name='update_course'),
    path('delete-course/<slug:course_slug>/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('create-category/', views.CategoryCreateView.as_view(), name='create_category'),
    path('update-category/<slug:category_slug>/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('delete-category/<slug:category_slug>/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('create-group/', views.GroupCreateView.as_view(), name='create_group'),
    path('update-group/<slug:group_slug>/', views.GroupUpdateView.as_view(), name='update_group'),
    path('delete-group/<slug:group_slug>/', views.GroupDeleteView.as_view(), name='delete_group'),
    path('my-courses/', views.StudentCoursesListView.as_view(), name='student_courses'),
    path('category/<slug:category_slug>/', views.CourseByCategoryListView.as_view(), name='course_by_category'),
    path('registration-requests/', views.RegistrationRequestListView.as_view(), name='registration_requests'),
    path('delete-request/<int:pk>/', views.RegistrationRequestDeleteView.as_view(), name='delete_request'),
    path('add-to-group/<slug:course_slug>/<int:user_id>/', views.add_student_to_group, name='add_student_to_group'),
    path('<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/register/', views.register_registration_request, name='register_registration_request'),
    path('<slug:course_slug>/course-request/', views.register_course_request, name='register_course_request'),
    path(
        'send-registration-link/<str:email>/<slug:course_slug>/',
        views.send_registration_link, name='send_registration_link',
    ),
]
