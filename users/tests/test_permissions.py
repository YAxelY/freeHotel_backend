from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from models import User
from ..models import HotelOwner

class PermissionTests(APITestCase):
    def test_hotel_owner_permissions(self):
        owner_user = User.objects.create_user(email='owner@test.com', is_hotel_owner=True)
        self.client.force_authenticate(user=owner_user)
        response = self.client.post('/api/hotels/', {'name': 'Test Hotel'})
        self.assertEqual(response.status_code, 201)