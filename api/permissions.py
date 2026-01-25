from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


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




# Custom Permission: Admin can do anything, Users can only Read
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff