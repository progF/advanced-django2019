from rest_framework import permissions

class UserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class DocumentPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        project = request.user.projects
        return obj.creator == request.user or project.creator == request.user or request.user.id in project.members__id


