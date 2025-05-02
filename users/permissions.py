from rest_framework import permissions
from hotels.models import Hotel, Room  

class IsHotelOwner(permissions.BasePermission):
    """Vérifie si l'utilisateur est le propriétaire de l'hôtel"""
    def has_object_permission(self, request, view, obj):
        # Pour les Hôtels
        if isinstance(obj, Hotel):
            return obj.owner.user == request.user
        
        # Pour les Chambres (via la relation Hotel)
        if isinstance(obj, Room):
            return obj.hotel.owner.user == request.user
        
        return False
    
# permissions.py
class CanManageHotel(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_hotel_owner
        return True


class IsSelfOrAdmin(permissions.BasePermission):
    """Allow users to edit their own profile"""
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class IsHotelOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.is_hotel_owner and obj.user == request.user)