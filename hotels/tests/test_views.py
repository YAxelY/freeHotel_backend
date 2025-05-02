from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Hotel

class HotelAPITests(APITestCase):
    def test_hotel_list(self):
        url = reverse('hotels:hotel-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)