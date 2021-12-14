from rest_framework import permissions


class CategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        # @TODO Подумать как сделать лучше
        # if request.user.role == 'admin' or request.user.is_staff:
        if request.user.is_staff:
            return True

        return False
