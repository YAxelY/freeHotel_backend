from rest_framework import generics, permissions
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationCreateView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # This will automatically set the user from the request
        serializer.save()

class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Hotel owner or admin: see all reservations for their hotels
        if hasattr(user, 'hotelowner') or user.is_staff or user.is_superuser:
            from hotels.models import Hotel
            hotel_ids = Hotel.objects.filter(owner=user.hotelowner).values_list('id', flat=True)
            return Reservation.objects.filter(room__hotel_id__in=hotel_ids).select_related('room')
        # Regular client: only their own reservations
        return Reservation.objects.filter(user=user).select_related('room')
    
class ReservationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reservation.objects.all()

    def get_queryset(self):
        user = self.request.user
        # Hotel owner or admin: can delete any reservation for their hotels
        if hasattr(user, 'hotelowner') or user.is_staff or user.is_superuser:
            from hotels.models import Hotel
            hotel_ids = Hotel.objects.filter(owner=user.hotelowner).values_list('id', flat=True)
            return Reservation.objects.filter(room__hotel_id__in=hotel_ids).select_related('room')
        # Regular client: only their own reservations
        return Reservation.objects.filter(user=user).select_related('room')
    
    

