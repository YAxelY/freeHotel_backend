from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from users.models import HotelOwner

User = get_user_model()

class PermissionTests(APITestCase):
    def setUp(self):
        # Créer l'utilisateur propriétaire avec référence à l'instance
        self.owner_user = User.objects.create_user(
            email='owner@test.com',
            password='testpass',
            is_hotel_owner=True
        )
        self.owner = HotelOwner.objects.create(
            user=self.owner_user,  # Utiliser self.owner_user
            business_name="Test Business",
            contact_number="+111111111"
            )
    def test_hotel_owner_permissions(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('hotels:hotel-list')
        data = {
            'name': 'Test Hotel',
            'location': 'Test Location',
            'description': 'Description de test',
            'amenities': []
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_regular_user_permissions(self):
        regular_user = User.objects.create_user(
            email='user@test.com', 
            password='testpass'
        )
        self.client.force_authenticate(user=regular_user)
        url = reverse('hotels:hotel-list')
        response = self.client.post(url, {
            'name': 'Unauthorized Hotel',
            'address': '456 Blocked Ave'
        })
        self.assertEqual(response.status_code, 403)