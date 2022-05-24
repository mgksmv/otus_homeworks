from django.urls import path

from . import views

app_name = 'onlineschool'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='courses'),
    path('search/', views.SearchCourseListView.as_view(), name='search'),
    path('schedule/', views.ScheduleListView.as_view(), name='schedule'),
    path('create-course/', views.CourseCreateView.as_view(), name='create_course'),
    path('update-course/<slug:course_slug>/', views.CourseUpdateView.as_view(), name='update_course'),
    path('delete-course/<slug:course_slug>/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('create-category/', views.CategoryCreateView.as_view(), name='create_category'),
    path('update-category/<slug:category_slug>/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('delete-category/<slug:category_slug>/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('create-group/', views.GroupCreateView.as_view(), name='create_group'),
    path('update-group/<slug:group_slug>/', views.GroupUpdateView.as_view(), name='update_group'),
    path('delete-group/<slug:group_slug>/', views.GroupDeleteView.as_view(), name='delete_group'),
    path('<slug:course_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('category/<slug:category_slug>/', views.CourseByCategoryListView.as_view(), name='course_by_category'),
]
