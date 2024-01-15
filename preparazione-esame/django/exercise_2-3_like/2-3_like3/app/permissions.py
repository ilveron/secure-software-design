from rest_framework import permissions


class IsPostEditorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or (request.method in permissions.SAFE_METHODS and
                                         request.user.groups.filter(name__in=['Customers', 'Reviewers', 'Analysts'])):
            return True
        return request.groups.filter(name__in=['Managers', 'Sellers', 'Suppliers'])
