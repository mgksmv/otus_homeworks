from rest_framework.permissions import BasePermission


class IsTeacherPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_type == '1'
        return request.user.is_authenticated


class IsStudentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_type == '2'
        return request.user.is_authenticated
