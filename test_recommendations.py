#!/usr/bin/env python
"""
Simple test script to verify the recommendation system works
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recommendation.services import RecommendationEngine
from hotels.models import Room, Hotel
from users.models import User

def test_recommendation_system():
    """Test the recommendation system"""
    print("Testing Recommendation System...")
    
    # Test 1: Check if we can create a RecommendationEngine
    try:
        engine = RecommendationEngine()
        print("✅ RecommendationEngine created successfully")
    except Exception as e:
        print(f"❌ Failed to create RecommendationEngine: {e}")
        return False
    
    # Test 2: Check if we can get popular rooms
    try:
        popular_rooms = engine.get_popular_rooms(limit=3)
        print(f"✅ Popular rooms query successful: {len(popular_rooms)} rooms found")
    except Exception as e:
        print(f"❌ Failed to get popular rooms: {e}")
        return False
    
    # Test 3: Check if we can get location recommendations
    try:
        location_hotels = engine.get_location_recommendations("Paris")
        print(f"✅ Location recommendations query successful: {len(location_hotels)} hotels found")
    except Exception as e:
        print(f"❌ Failed to get location recommendations: {e}")
        return False
    
    # Test 4: Check if we can get room recommendations (if we have rooms)
    try:
        rooms = Room.objects.filter(is_available=True)[:1]
        if rooms:
            room = rooms[0]
            recommendations = engine.get_recommendations(room, None)
            print(f"✅ Room recommendations query successful: {len(recommendations)} recommendations found")
        else:
            print("⚠️  No rooms available for testing room recommendations")
    except Exception as e:
        print(f"❌ Failed to get room recommendations: {e}")
        return False
    
    print("🎉 All recommendation system tests passed!")
    return True

if __name__ == "__main__":
    test_recommendation_system() 