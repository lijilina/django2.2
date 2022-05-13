from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限验证，只有允许对象的创建才能修改数据
    """
    def has_object_permission(self, request, view, obj):

        # permissions.SAFE_METHODS 的值为 ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
