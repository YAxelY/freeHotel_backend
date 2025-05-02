from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from reservations.models import Reservation
from users.models import User
from hotels.models import Hotel, Room, HotelOwner

class ReservationViewTests(APITestCase):
    def setUp(self):
        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        
        # Create hotel owner
        self.owner = HotelOwner.objects.create(
            user=User.objects.create_user(
                email='owner@example.com',
                password='ownerpass123',
                is_hotel_owner=True
            ),
            business_name="Test Hotel"
        )
        
        # Create hotel and room
        self.hotel = Hotel.objects.create(
            owner=self.owner,
            name="Grand Hotel",
            location="Paris"
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type="Deluxe",
            price_per_night=200.00,
            capacity=2
        )
        
        # Valid reservation data
        self.valid_data = {
            "room": self.room.id,
            "check_in": date.today().isoformat(),
            "check_out": (date.today() + timedelta(days=3)).isoformat()
        }

    def test_create_reservation_unauthenticated(self):
        url = reverse('reservations:reservation-create')
        response = self.client.post(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reservation_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations:reservation-create')
        response = self.client.post(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().user, self.user)
    def test_list_reservations(self):
        # Create a reservation
        Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=2)
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations:reservation-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the paginated 'results' array
        self.assertEqual(len(response.data['results']), 1)  # Changed this line
        self.assertEqual(response.data['count'], 1)  # Add count verification
        
    def test_invalid_dates_in_request(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            "room": self.room.id,
            "check_in": (date.today() + timedelta(days=3)).isoformat(),
            "check_out": date.today().isoformat()
        }
        url = reverse('reservations:reservation-create')
        response = self.client.post(url, invalid_data)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(
            response.data['non_field_errors'][0],
            "Check-out must be after check-in"
        )

    def test_delete_reservation(self):
        reservation = Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=2)
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations:reservation-detail', kwargs={'pk': reservation.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)