from django.db.models import Q, Count
from hotels.models import Room, Hotel
from decimal import Decimal

class RecommendationEngine:
    def __init__(self):
        pass
    
    def get_recommendations(self, target_room, user):
        """
        Get room recommendations based on:
        1. Same hotel (if user liked this hotel)
        2. Similar room type and price range
        3. Popular rooms in the same location
        4. Rooms with good ratings
        """
        recommendations = []
        
        # 1. Other rooms in the same hotel (exclude the target room)
        same_hotel_rooms = Room.objects.filter(
            hotel=target_room.hotel,
            is_available=True
        ).exclude(id=target_room.id)[:3]
        recommendations.extend(same_hotel_rooms)
        
        # 2. Similar room type and price range (±20% of target room price)
        price_min = target_room.price_per_night * Decimal('0.8')
        price_max = target_room.price_per_night * Decimal('1.2')
        
        similar_rooms = Room.objects.filter(
            room_type=target_room.room_type,
            price_per_night__gte=price_min,
            price_per_night__lte=price_max,
            is_available=True
        ).exclude(id=target_room.id)[:3]
        recommendations.extend(similar_rooms)
        
        # 3. Rooms in the same location (by hotel rating)
        location_rooms = Room.objects.filter(
            hotel__location__iexact=target_room.hotel.location,
            is_available=True
        ).exclude(id=target_room.id).order_by('-hotel__rating')[:3]
        recommendations.extend(location_rooms)
        
        # 4. Rooms with good ratings (if hotel has rating)
        if target_room.hotel.rating and target_room.hotel.rating >= 4.0:
            high_rated_rooms = Room.objects.filter(
                hotel__rating__gte=4.0,
                is_available=True
            ).exclude(id=target_room.id)[:2]
            recommendations.extend(high_rated_rooms)
        
        # Remove duplicates and limit results
        seen_ids = set()
        unique_recommendations = []
        for room in recommendations:
            if room.id not in seen_ids and len(unique_recommendations) < 5:
                seen_ids.add(room.id)
                unique_recommendations.append(room)
        
        return unique_recommendations
    
    def get_location_recommendations(self, location):
        """
        Get hotel recommendations for a specific location
        """
        return Hotel.objects.filter(
            location__iexact=location,
            status='published'
        ).order_by('-rating')[:10]
    
    def get_popular_rooms(self, limit=5):
        """
        Get most popular rooms based on hotel rating and availability
        """
        return Room.objects.filter(
            is_available=True
        ).order_by('-hotel__rating')[:limit]