from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from users.permissions import CanManageHotel, IsHotelOwner
from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer

from users.models import User
from .filters import HotelFilter 

class HotelListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'location', 'description']
    filterset_class = HotelFilter  
    filterset_fields = ['amenities']
    permission_classes = [CanManageHotel]

    def get_queryset(self):
        queryset = Hotel.objects.all()
        if self.request.query_params.get('has_available_rooms'):
            queryset = queryset.filter(room__is_available=True).distinct()
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_hotel_owner:
            serializer.save(owner=self.request.user.hotelowner)

class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsHotelOwner]

class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsHotelOwner]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel__id=hotel_id)

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'])
        serializer.save(hotel=hotel)

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsHotelOwner]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel__id=hotel_id)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


from .filters import HotelFilter

class HotelListCreateView(generics.ListCreateAPIView):
    filterset_class = HotelFilter