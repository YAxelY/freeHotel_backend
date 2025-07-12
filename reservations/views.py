from rest_framework import generics, permissions, status as drf_status
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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
    
class ReservationStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({'detail': 'Reservation not found.'}, status=drf_status.HTTP_404_NOT_FOUND)
        user = request.user
        # Only the reservation owner or staff can update
        if reservation.user != user and not (user.is_staff or user.is_superuser):
            return Response({'detail': 'Not authorized.'}, status=drf_status.HTTP_403_FORBIDDEN)
        new_status = request.data.get('status')
        if new_status not in ['SUCCESS', 'CONFIRMED', 'CANCELED']:
            return Response({'detail': 'Invalid status.'}, status=drf_status.HTTP_400_BAD_REQUEST)
        # Only allow PENDING -> SUCCESS or CONFIRMED or CANCELED
        if reservation.status != 'PENDING':
            return Response({'detail': 'Can only update status from PENDING.'}, status=drf_status.HTTP_400_BAD_REQUEST)
        reservation.status = new_status
        reservation.save()
        return Response({'detail': 'Status updated.', 'status': reservation.status})
    
    

