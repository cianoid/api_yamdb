from rest_framework import permissions, status

from api.exceptions import CustomAPIException


class AdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        jwt = request.META.get('HTTP_AUTHORIZATION')

        if jwt is None:
            raise CustomAPIException(
                detail='Необходим JWT-токен',
                status_code=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_authenticated:
            return False

        # @TODO Подумать как сделать лучше
        # if request.user.is_staff:
        if request.user.role == 'admin' or request.user.is_staff:
            return True

        return False


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        return False


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
