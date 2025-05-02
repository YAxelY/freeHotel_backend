from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer
from .permissions import CanManageHotel, IsHotelOwner
from rest_framework.exceptions import PermissionDenied
from .filters import HotelFilter

class HotelListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'location', 'description']
    filterset_class = HotelFilter
    permission_classes = [CanManageHotel]
    

    def get_queryset(self):
        queryset = Hotel.objects.all()
        
        if self.request.query_params.get('has_available_rooms') == 'true':
            return queryset.filter(
                rooms__is_available=True
            ).distinct()
            
        return queryset
    

    def perform_create(self, serializer):
        # Vérification supplémentaire de sécurité
        if not self.request.user.is_hotel_owner:
            raise PermissionDenied("Seuls les propriétaires peuvent créer des hôtels")
        serializer.save(owner=self.request.user.hotelowner)

class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsHotelOwner]
    lookup_field = 'pk'

class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsHotelOwner]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel__id=hotel_id)

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'])
        self.check_object_permissions(self.request, hotel)
        serializer.save(hotel=hotel)

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsHotelOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel__id=hotel_id)
    
    def perform_create(self, serializer):
        # Get hotel and verify ownership
        hotel = get_object_or_404(
            Hotel,
            id=self.kwargs['hotel_id'],
            owner__user=self.request.user  # Critical security check
        )
        serializer.save(hotel=hotel)