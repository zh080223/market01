from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 判断是否是管理员
        if request.user.is_superuser:
            return True
        # 不是管理员就判断obj是否是自己
        return obj == request.user


class AddressPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user
