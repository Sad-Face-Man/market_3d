from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только автору редактировать/удалять объект.
    Остальные могут только просматривать.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешены безопасные методы (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешено только автору
        return obj.author == request.user
