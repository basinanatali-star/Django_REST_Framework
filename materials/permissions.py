from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Модераторы").exists()
        )


class IsModeratorOrOwner(BasePermission):


    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_moderator = request.user.groups.filter(
            name="Модераторы"
        ).exists()

        if is_moderator and request.method in ["POST", "DELETE"]:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        is_moderator = request.user.groups.filter(
            name="Модераторы"
        ).exists()

        if is_moderator:
            return True

        return obj.owner == request.user