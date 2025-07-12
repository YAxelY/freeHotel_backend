from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from hotels.models import Room, Hotel
from hotels.serializers import RoomSerializer, HotelSerializer
from .services import RecommendationEngine
from django.contrib.auth import get_user_model
from reservations.models import Reservation

# Room-based recommendations
class RoomRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = get_object_or_404(Room, id=room_id)
            engine = RecommendationEngine()
            recommendations = engine.get_recommendations(room, request.user)
            serializer = RoomSerializer(recommendations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Failed to get recommendations", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Location-based hotel recommendations
class LocationHotelRecommendationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, location):
        try:
            engine = RecommendationEngine()
            hotels = engine.get_location_recommendations(location)
            serializer = HotelSerializer(hotels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Failed to get location recommendations", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# User-based room recommendations (personalized)
class UserRoomRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            engine = RecommendationEngine()
            
            # Try to get recommendations based on user's last booking
            last_reservation = Reservation.objects.filter(client_email=user.email).order_by('-check_in').first()
            
            if last_reservation and last_reservation.room:
                # Get recommendations based on the last booked room
                recommendations = engine.get_recommendations(last_reservation.room, user)
            else:
                # Fallback: get popular rooms if user has no booking history
                recommendations = engine.get_popular_rooms(limit=5)
            
            serializer = RoomSerializer(recommendations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": "Failed to get personalized recommendations", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Popular room recommendations (no authentication required)
class PopularRoomRecommendationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            engine = RecommendationEngine()
            recommendations = engine.get_popular_rooms(limit=5)
            serializer = RoomSerializer(recommendations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Failed to get popular recommendations", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
