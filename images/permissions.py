from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

from apartments.models import Apartment


class IsOwnerOrForbidden(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool | PermissionDenied:
        apartment_id = view.kwargs.get("advertisement_id")
        apartment_obj = Apartment.objects.get(id=apartment_id)

        if apartment_obj and apartment_obj.owner_id == request.user.id:
            return True
        else:
            raise PermissionDenied("You are not the owner of this apartment")
