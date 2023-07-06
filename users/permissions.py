from rest_framework import permissions
from .models import User
from rest_framework.views import View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated and obj == request.user:
            return True
        return False


class IsAccountEmployee(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_authenticated and request.user.employee


class IsAccountEmployeeExceptGet(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.employee


class IsAccountOwnerOrEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated and obj == request.user:
            return True
        if request.user.is_authenticated and request.user.employee:
            return True
        return False


class IsAccountEmployeExceptPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            and request.user.is_authenticated
            and request.user.employee
        ):
            return True
        if request.method in "POST":
            return True
        return False
