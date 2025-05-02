from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from reservations.models import Reservation
from users.models import User
from hotels.models import Hotel, Room, HotelOwner

class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Create hotel owner
        cls.owner = HotelOwner.objects.create(
            user=User.objects.create_user(
                email='owner@example.com',
                password='ownerpass123',
                is_hotel_owner=True
            ),
            business_name="Test Hotel"
        )
        
        # Create hotel and room
        cls.hotel = Hotel.objects.create(
            owner=cls.owner,
            name="Grand Hotel",
            location="Paris"
        )
        cls.room = Room.objects.create(
            hotel=cls.hotel,
            room_number="101",
            room_type="Deluxe",
            price_per_night=200.00,
            capacity=2
        )

    def test_create_reservation(self):
        reservation = Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=3),
            status='PENDING'
        )
        self.assertEqual(str(reservation), f"test@example.com - 101 ({date.today()} to {date.today() + timedelta(days=3)})")

    def test_invalid_dates(self):
        with self.assertRaises(ValidationError):
            reservation = Reservation(
                user=self.user,
                room=self.room,
                check_in=date.today() + timedelta(days=3),
                check_out=date.today()
            )
            reservation.full_clean()

    def test_overlapping_reservations(self):
        # Create first reservation
        Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=3),
            status='CONFIRMED'
        )
        
        # Try overlapping reservation
        with self.assertRaises(ValidationError):
            reservation = Reservation(
                user=self.user,
                room=self.room,
                check_in=date.today() + timedelta(days=1),
                check_out=date.today() + timedelta(days=4)
            )
            reservation.full_clean()