from rest_framework.permissions import BasePermission
import main.views


class specialpermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return False