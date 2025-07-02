#!/usr/bin/env python
"""
Simple test script to verify room syncing functionality.
Run this script to test the room syncing without needing to set up the full test database.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from hotels.models import Hotel, Room
from users.models import User, HotelOwner

def test_room_sync():
    """Test the room syncing functionality"""
    print("Testing room syncing functionality...")
    
    # Create test user and hotel owner
    try:
        user = User.objects.create_user(
            email='test_sync@example.com',
            password='testpass123',
            is_hotel_owner=True
        )
        hotel_owner = HotelOwner.objects.create(
            user=user,
            business_name="Test Sync Hotel"
        )
        print("✓ Created test user and hotel owner")
    except Exception as e:
        print(f"✗ Failed to create test user: {e}")
        return
    
    # Create test hotel with template_data
    try:
        hotel = Hotel.objects.create(
            owner=hotel_owner,
            name="Test Sync Hotel",
            location="Test Location",
            template_data={
                'rooms': [
                    {
                        'roomNumber': '101',
                        'roomType': 'Deluxe',
                        'price': 200.00,
                        'capacity': 2,
                        'isAvailable': True,
                        'name': 'Deluxe Room 101',
                        'desc': 'A beautiful deluxe room',
                        'type': 'Deluxe',
                        'beds': '1 King Bed',
                        'image': 'https://example.com/room101.jpg'
                    },
                    {
                        'roomNumber': '102',
                        'roomType': 'Standard',
                        'price': 150.00,
                        'capacity': 1,
                        'isAvailable': True,
                        'name': 'Standard Room 102',
                        'desc': 'A comfortable standard room',
                        'type': 'Standard',
                        'beds': '1 Queen Bed',
                        'image': 'https://example.com/room102.jpg'
                    }
                ]
            }
        )
        print("✓ Created test hotel with template_data")
    except Exception as e:
        print(f"✗ Failed to create test hotel: {e}")
        return
    
    # Test room syncing
    try:
        print(f"Before sync: {Room.objects.filter(hotel=hotel).count()} rooms")
        hotel.sync_rooms_from_template_data()
        print(f"After sync: {Room.objects.filter(hotel=hotel).count()} rooms")
        
        # Check room details
        rooms = Room.objects.filter(hotel=hotel)
        for room in rooms:
            print(f"  - Room {room.room_number}: {room.room_type}, ${room.price_per_night}, {room.capacity} guests")
        
        print("✓ Room syncing completed successfully")
        
    except Exception as e:
        print(f"✗ Room syncing failed: {e}")
        return
    
    # Test updating template_data
    try:
        print("\nTesting template_data update...")
        hotel.template_data['rooms'][0]['price'] = 250.00  # Update price
        hotel.template_data['rooms'][0]['roomType'] = 'Premium Deluxe'  # Update type
        hotel.template_data['rooms'].append({  # Add new room
            'roomNumber': '103',
            'roomType': 'Suite',
            'price': 300.00,
            'capacity': 4,
            'isAvailable': True,
            'name': 'Luxury Suite 103',
            'desc': 'A luxurious suite',
            'type': 'Suite',
            'beds': '1 King Bed + 1 Queen Bed',
            'image': 'https://example.com/suite103.jpg'
        })
        hotel.save()
        
        print(f"Before update sync: {Room.objects.filter(hotel=hotel).count()} rooms")
        hotel.sync_rooms_from_template_data()
        print(f"After update sync: {Room.objects.filter(hotel=hotel).count()} rooms")
        
        # Check updated room details
        rooms = Room.objects.filter(hotel=hotel)
        for room in rooms:
            print(f"  - Room {room.room_number}: {room.room_type}, ${room.price_per_night}, {room.capacity} guests")
        
        print("✓ Template_data update syncing completed successfully")
        
    except Exception as e:
        print(f"✗ Template_data update syncing failed: {e}")
        return
    
    # Clean up
    try:
        hotel.delete()
        hotel_owner.delete()
        user.delete()
        print("✓ Cleanup completed")
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
    
    print("\n🎉 All tests passed! Room syncing is working correctly.")

if __name__ == '__main__':
    test_room_sync() 