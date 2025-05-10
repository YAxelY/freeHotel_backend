from rest_framework import generics
from hotels.models import Room
from hotels.serializers import RoomSerializer
from .services import RecommendationEngine

class RoomRecommendationView(generics.ListAPIView):
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        room_id = self.kwargs['room_id']
        user = self.request.user
        engine = RecommendationEngine()
        
        try:
            target_room = Room.objects.get(id=room_id)
            return engine.get_recommendations(target_room, user)
        except Room.DoesNotExist:
            return Room.objects.none()