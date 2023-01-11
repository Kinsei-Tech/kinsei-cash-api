from rest_framework import permissions
from .models import Category
from rest_framework.views import View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Category) -> bool:
        return request.user.is_authenticated and obj.user == request.user
