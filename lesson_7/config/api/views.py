from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse


class APIRootView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response({
            'auth': {
                'users': reverse('accounts_api:user-list', request=request),
            },
            'onlineschool': {
                'courses': reverse('onlineschool_api:course-list', request=request),
                'schedule': reverse('onlineschool_api:schedule-list', request=request),
                'categories': reverse('onlineschool_api:category-list', request=request),
                'teachers': reverse('onlineschool_api:teacher-list', request=request),
                'students': reverse('onlineschool_api:student-list', request=request),
            },
            'for-teachers': {
                'registration-requests': reverse('onlineschool_api:registrationrequest-list', request=request),
                'course-requests': reverse('onlineschool_api:courserequest-list', request=request),
            },
            'for-students': {
                'student-courses': reverse('onlineschool_api:student_courses-list', request=request),
            },
        })
