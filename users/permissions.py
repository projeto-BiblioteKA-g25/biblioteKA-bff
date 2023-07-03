from rest_framework import permissions
from .models import User
from rest_framework.views import View


class IsAccountEmployee(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.employee


class IsAccountUser(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj == request.user
