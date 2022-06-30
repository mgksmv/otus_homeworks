from rest_framework.permissions import BasePermission


class IsTeacherPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.user_type == '1')
        return bool(request.user.is_authenticated)


class IsStudentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.user_type == '2')
        return bool(request.user.is_authenticated)
