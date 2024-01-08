from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsPostEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='post_editors').exists()


method2perm = {
    'POST': 'add',
    'PUT': 'change',
    'PATCH': 'change',
    'DELETE': 'delete',
    'GET': 'view',
    'HEAD': 'view',
    'OPTIONS': 'view',
}


class IsPermittedOnPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in method2perm:
            return False
        return request.user.has_perm(f'posts.{method2perm[request.method]}_post')