from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError




from .models import HotelOwner, Hotel, Room

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_regular_user(self):
        user = User.objects.create_user(
            email='guest@test.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'guest@test.com')
        self.assertFalse(user.is_hotel_owner)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_hotel_owner_user(self):
        owner_user = User.objects.create_user(
            email='owner@test.com',
            password='ownerpass123',
            is_hotel_owner=True
        )
        self.assertTrue(owner_user.is_hotel_owner)
        self.assertEqual(owner_user.email, 'owner@test.com')

    def test_email_uniqueness(self):
        User.objects.create_user(
            email='duplicate@test.com',
            password='pass123'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='duplicate@test.com',
                password='pass456'
            )
        
    def test_email_only_user(self):  # Properly indented
        user = User.objects.create_user(
            email='emailonly@test.com',
            password='testpass'
        )
        self.assertIsNone(user.username)
        self.assertEqual(user.email, 'emailonly@test.com')

    def test_username_only_user(self):  # Properly indented
        user = User.objects.create_user(
            username='user123',
            password='testpass'
        )
        self.assertIsNone(user.email)
        self.assertEqual(user.username, 'user123')

    def test_both_fields_user(self):  # Properly indented
        user = User.objects.create_user(
            username='user456',
            email='both@test.com',
            password='testpass'
        )
        self.assertEqual(user.username, 'user456')
        self.assertEqual(user.email, 'both@test.com')

    def test_username_login(self):  # Properly indented and fixed
        user = User.objects.create_user(
            username='testlogin',
            password='testpass'
        )
        from django.contrib.auth import authenticate
        auth_user = authenticate(username='testlogin', password='testpass')
        self.assertEqual(auth_user, user)

    def test_superuser_creation(self):
            admin_user = User.objects.create_superuser(
                email='admin@test.com',
                password='adminpass'
            )
            self.assertTrue(admin_user.is_superuser)
            self.assertTrue(admin_user.is_staff)

class HotelOwnerModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@test.com',
            password='testpass',
            is_hotel_owner=True
        )

    def test_hotel_owner_creation(self):
        owner = HotelOwner.objects.create(
            user=self.user,
            business_name="Luxury Stays",
            contact_number="+123456789"
        )
        self.assertEqual(owner.user.email, 'owner@test.com')
        self.assertEqual(owner.business_name, "Luxury Stays")

class HotelModelTests(TestCase):
    def setUp(self):
        owner_user = User.objects.create_user(
            email='hotelowner@test.com',
            password='testpass',
            is_hotel_owner=True
        )
        self.owner = HotelOwner.objects.create(
            user=owner_user,
            business_name="Grand Hotels",
            contact_number="+11111111"
        )

    def test_hotel_creation(self):
        hotel = Hotel.objects.create(
            owner=self.owner,
            name="Paradise Resort",
            location="Maldives",
            description="Luxury beach resort",
            rating=4.8,
            amenities=["Pool", "Spa"]
        )
        self.assertEqual(hotel.owner.business_name, "Grand Hotels")
        self.assertIn("Spa", hotel.amenities)

    def test_rating_validation(self):
        hotel = Hotel(
            owner=self.owner,
            name="Invalid Rating",
            location="Test",
            description="Test",
            rating=5.1
        )
        with self.assertRaises(ValidationError):
            hotel.full_clean()

class RoomModelTests(TestCase):
    def setUp(self):
        owner_user = User.objects.create_user(
            email='rooms@test.com',
            password='testpass',
            is_hotel_owner=True
        )
        owner = HotelOwner.objects.create(
            user=owner_user,
            business_name="Room Experts",
            contact_number="+22222222"
        )
        self.hotel = Hotel.objects.create(
            owner=owner,
            name="Room Test Hotel",
            location="Test",
            description="Test",
            rating=4.0
        )

    def test_room_creation(self):
        room = Room.objects.create(
            hotel=self.hotel,
            room_number="301",
            room_type="Deluxe",
            price_per_night=299.99,
            capacity=2
        )
        self.assertEqual(room.room_type, "Deluxe")
        self.assertAlmostEqual(room.price_per_night, 299.99, places=2)
        self.assertTrue(room.is_available)

    def test_availability_default(self):
        room = Room.objects.create(
            hotel=self.hotel,
            room_number="401",
            room_type="Standard",
            price_per_night=99.99,
            capacity=1
        )
        self.assertTrue(room.is_available)