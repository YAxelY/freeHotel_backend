from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import HotelOwner

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

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

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
        self.assertEqual(str(owner), "Luxury Stays")