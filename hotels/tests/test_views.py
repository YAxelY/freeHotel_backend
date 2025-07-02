from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Hotel, Room
from users.models import User, HotelOwner

class HotelAPITests(APITestCase):
    def setUp(self):
        # Create test user and hotel owner
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_hotel_owner=True
        )
        self.hotel_owner = HotelOwner.objects.create(
            user=self.user,
            business_name="Test Hotel Business"
        )
        
        # Create test hotel
        self.hotel = Hotel.objects.create(
            owner=self.hotel_owner,
            name="Test Hotel",
            location="Test Location",
            template_data={
                'rooms': [
                    {
                        'roomNumber': '101',
                        'roomType': 'Deluxe',
                        'price': 200.00,
                        'capacity': 2,
                        'isAvailable': True
                    },
                    {
                        'roomNumber': '102',
                        'roomType': 'Standard',
                        'price': 150.00,
                        'capacity': 1,
                        'isAvailable': True
                    }
                ]
            }
        )

    def test_hotel_list(self):
        url = reverse('hotels:hotel-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_room_sync_on_publish(self):
        """Test that rooms are synced from template_data when hotel is published"""
        self.client.force_authenticate(user=self.user)
        
        # Initially no rooms should exist
        self.assertEqual(Room.objects.filter(hotel=self.hotel).count(), 0)
        
        # Publish the hotel
        url = reverse('hotels:hotel-publish', kwargs={'pk': self.hotel.pk})
        response = self.client.patch(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Check that rooms were created from template_data
        rooms = Room.objects.filter(hotel=self.hotel)
        self.assertEqual(rooms.count(), 2)
        
        # Check room details
        room_101 = rooms.get(room_number='101')
        self.assertEqual(room_101.room_type, 'Deluxe')
        self.assertEqual(float(room_101.price_per_night), 200.00)
        self.assertEqual(room_101.capacity, 2)
        self.assertTrue(room_101.is_available)
        
        room_102 = rooms.get(room_number='102')
        self.assertEqual(room_102.room_type, 'Standard')
        self.assertEqual(float(room_102.price_per_night), 150.00)
        self.assertEqual(room_102.capacity, 1)
        self.assertTrue(room_102.is_available)

    def test_room_sync_on_update(self):
        """Test that rooms are synced when hotel template_data is updated"""
        self.client.force_authenticate(user=self.user)
        
        # First publish to create initial rooms
        url = reverse('hotels:hotel-publish', kwargs={'pk': self.hotel.pk})
        self.client.patch(url)
        
        # Update template_data with modified rooms
        updated_template_data = {
            'rooms': [
                {
                    'roomNumber': '101',
                    'roomType': 'Premium Deluxe',  # Updated
                    'price': 250.00,  # Updated
                    'capacity': 3,  # Updated
                    'isAvailable': True
                },
                {
                    'roomNumber': '103',  # New room
                    'roomType': 'Suite',
                    'price': 300.00,
                    'capacity': 4,
                    'isAvailable': True
                }
                # Room 102 removed
            ]
        }
        
        # Update hotel
        url = reverse('hotels:hotel-detail', kwargs={'pk': self.hotel.pk})
        response = self.client.patch(url, {
            'template_data': updated_template_data
        }, format='json')
        
        self.assertEqual(response.status_code, 200)
        
        # Check that rooms were synced correctly
        rooms = Room.objects.filter(hotel=self.hotel)
        self.assertEqual(rooms.count(), 2)
        
        # Check updated room 101
        room_101 = rooms.get(room_number='101')
        self.assertEqual(room_101.room_type, 'Premium Deluxe')
        self.assertEqual(float(room_101.price_per_night), 250.00)
        self.assertEqual(room_101.capacity, 3)
        
        # Check new room 103
        room_103 = rooms.get(room_number='103')
        self.assertEqual(room_103.room_type, 'Suite')
        self.assertEqual(float(room_103.price_per_night), 300.00)
        self.assertEqual(room_103.capacity, 4)
        
        # Room 102 should be deleted
        self.assertFalse(Room.objects.filter(room_number='102', hotel=self.hotel).exists())

    def test_room_sync_with_invalid_data(self):
        """Test that invalid room data is handled gracefully"""
        self.client.force_authenticate(user=self.user)
        
        # Update with invalid room data
        invalid_template_data = {
            'rooms': [
                {
                    'roomNumber': '101',
                    'roomType': 'Valid Room',
                    'price': 200.00,
                    'capacity': 2,
                    'isAvailable': True
                },
                {
                    'roomNumber': '',  # Invalid - empty room number
                    'roomType': 'Invalid Room',
                    'price': 150.00,
                    'capacity': 1,
                    'isAvailable': True
                },
                {
                    'roomNumber': '102',
                    'roomType': 'Another Valid Room',
                    'price': 'invalid_price',  # Invalid - string instead of number
                    'capacity': 1,
                    'isAvailable': True
                }
            ]
        }
        
        # Update hotel
        url = reverse('hotels:hotel-detail', kwargs={'pk': self.hotel.pk})
        response = self.client.patch(url, {
            'template_data': invalid_template_data
        }, format='json')
        
        self.assertEqual(response.status_code, 200)
        
        # Only valid rooms should be created
        rooms = Room.objects.filter(hotel=self.hotel)
        self.assertEqual(rooms.count(), 1)
        
        # Check that only the valid room exists
        room_101 = rooms.get(room_number='101')
        self.assertEqual(room_101.room_type, 'Valid Room')
        self.assertEqual(float(room_101.price_per_night), 200.00)