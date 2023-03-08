from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        is_admin = bool(request.user and request.user.is_staff)
        
        return request.method == 'GET' or is_admin

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if(request.method in permissions.SAFE_METHODS):
            return True # can view for get
        else:
            return request.user == obj.user # for non-get requests