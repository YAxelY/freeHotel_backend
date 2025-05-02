from rest_framework import permissions
from .models import Hotel, Room

class IsHotelOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # For creation (POST) - Check if user is hotel owner
        if request.method == 'POST':
            return request.user.is_hotel_owner
        return True

    def has_object_permission(self, request, view, obj):
        # For existing objects
        if isinstance(obj, Hotel):
            return obj.owner.user == request.user
        if isinstance(obj, Room):
            return obj.hotel.owner.user == request.user
        return False

class CanManageHotel(permissions.BasePermission):
    """Autorise la création uniquement aux propriétaires d'hôtel"""
    def has_permission(self, request, view):
        # Remplacer la vérification de view.action par request.method
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.is_hotel_owner
        return True