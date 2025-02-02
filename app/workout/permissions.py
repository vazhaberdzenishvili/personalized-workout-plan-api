from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission: Only admins can perform write operations,
    others can only read (GET requests).
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Allow all users to read data
        if request.method in SAFE_METHODS:
            return True
        # Allow only admin users to perform write operations
        return request.user.is_staff
