from rest_framework.permissions import BasePermission

class RoomBasePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

class ViewPermission(RoomBasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_viewable(request.user)

class WritePermission(RoomBasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_writable(request.user)

class AdminPermission(RoomBasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_administrable(request.user)
