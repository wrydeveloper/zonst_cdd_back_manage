from rest_framework import permissions


class AdminPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role != 'commerce':
            return False

        return True
