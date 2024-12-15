from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """自定义权限，只有管理员可以访问"""
    def has_permission(self, request, view):
        # 检查用户是否是管理员
        return request.user and request.user.is_superuser
