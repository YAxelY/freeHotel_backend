from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer
from .permissions import CanManageHotel, IsHotelOwner
from rest_framework.exceptions import PermissionDenied
from .filters import HotelFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone

class HotelListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'location', 'description']
    filterset_class = HotelFilter
    permission_classes = [CanManageHotel]
    

    def get_queryset(self):
        queryset = Hotel.objects.all()
        # Filter by owner for dashboard
        if self.request.user.is_authenticated and hasattr(self.request.user, 'hotelowner'):
            queryset = queryset.filter(owner=self.request.user.hotelowner)
        if self.request.query_params.get('has_available_rooms') == 'true':
            return queryset.filter(rooms__is_available=True).distinct()
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

class PublishHotelView(APIView):
    permission_classes = [IsHotelOwner]

    def patch(self, request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        self.check_object_permissions(request, hotel)
        # Set status to published and set published_at
        hotel.status = 'published'
        hotel.published_at = timezone.now()
        hotel.save()
        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PreviewHotelView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only owner can preview

    def get(self, request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        if hotel.owner != request.user.hotelowner:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

class PublicHotelListView(generics.ListAPIView):
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Hotel.objects.filter(status='published')