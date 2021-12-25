from rest_framework import permissions


class AdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_admin or user.is_staff:
            return True

        return False


class AdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin or request.user.is_staff:
            return True
        return False


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_staff or user.is_admin or user.is_moderator:
            return True

        return obj.author == user
