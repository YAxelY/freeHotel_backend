from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Hotel, Room, Review
from .serializers import HotelSerializer, RoomSerializer, ReviewSerializer
from .permissions import CanManageHotel, IsHotelOwner
from rest_framework.exceptions import PermissionDenied
from .filters import HotelFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, Count

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

    def perform_update(self, serializer):
        hotel = serializer.save()
        # No more sync_rooms_from_template_data
        # with transaction.atomic():
        #     hotel.sync_rooms_from_template_data()

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
        with transaction.atomic():
            hotel.status = 'published'
            hotel.published_at = timezone.now()
            hotel.save()
            # No more sync_rooms_from_template_data
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

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({'detail': 'You can only delete your own review.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class ReviewStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from .models import Review
        total = Review.objects.count()
        avg = Review.objects.aggregate(avg=Avg('stars'))['avg'] or 0
        # Per-star counts (1-5)
        star_counts = Review.objects.values('stars').annotate(count=Count('id'))
        star_dict = {i: 0 for i in range(1, 6)}
        for entry in star_counts:
            star_dict[entry['stars']] = entry['count']
        return Response({
            'average': round(avg, 2),
            'total': total,
            'stars': star_dict
        })