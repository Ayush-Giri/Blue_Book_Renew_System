from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission


# class IsActiveUser(BasePermission):
#     message = "Your account is disabled."
#
#     def has_permission(self, request, view):
#         return bool(
#             request.user
#             and request.user.is_authenticated
#             and request.user.is_active
#         )

from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    message = "Your account has been disabled."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )



class IsAdmin(BasePermission):
    message = "Admin access only."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )