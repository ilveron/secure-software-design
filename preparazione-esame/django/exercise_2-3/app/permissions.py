from rest_framework import permissions


class IsPostEditorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_superuser or (request.method in permissions.SAFE_METHODS and request.user.groups.filter(name__in=['TheTick', 'FutureMan', 'DoomPatrol']).exists()):
            return True
        return request.user.groups.filter(name__in=['Avengers', 'Xmen', 'AmericanGods']).exists()

    def has_object_permission(self, request, view, obj):
        if request.user == obj.post_editor:
            return True
