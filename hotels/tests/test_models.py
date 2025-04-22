from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Hotel, Room
from users.models import User, HotelOwner

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

    # Ajouter ici les tests Hotel...

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

    # Ajouter ici les tests Room...