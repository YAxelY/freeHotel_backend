from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from hotels.models import Room, Hotel
from hotels.serializers import RoomSerializer, HotelSerializer
from .services import RecommendationEngine
from django.contrib.auth import get_user_model

# Room-based recommendations
class RoomRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(room, request.user)
        serializer = RoomSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Location-based hotel recommendations
class LocationHotelRecommendationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, location):
        hotels = Hotel.objects.filter(location__iexact=location, status='published')
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# User-based room recommendations (personalized)
class UserRoomRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # For demo: recommend rooms based on user's last booking or search (expand as needed)
        last_room = Room.objects.filter(reservation__client_email=user.email).order_by('-reservation__check_in').first()
        if not last_room:
            return Response([], status=status.HTTP_200_OK)
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(last_room, user)
        serializer = RoomSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
