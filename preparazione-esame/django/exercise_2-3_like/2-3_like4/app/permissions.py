from rest_framework import permissions


class IsPostEditorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or (request.method in permissions.SAFE_METHODS and
                                     request.user.groups.filter(name__in=["Students", "Teachers", "Players"])):
            return True
        return request.user.groups.filter(name__in=["Developers", "Producers", "Critics"])
