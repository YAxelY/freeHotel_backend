from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTests(APITestCase):
    def test_user_registration(self):
        url = reverse('user-registration')
        data = {
            'email': 'test@example.com',
            'password': 'ComplexPass123!',
            'username': 'testuser'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        User.objects.create_user(email='test@example.com', password='testpass')
        url = reverse('api-token-auth')
        data = {
            'username_or_email': 'test@example.com',
            'password': 'testpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
    
    
    # test_views.py
def test_hotel_owner_registration(self):
    user = User.objects.create_user(email='test@example.com', password='testpass')
    self.client.force_authenticate(user=user)
    
    url = reverse('hotel-owner-registration')
    data = {
        'business_name': 'Test Hotel',
        'contact_number': '+1234567890'
    }
    
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, 201)
    self.assertTrue(user.is_hotel_owner)
    self.assertEqual(response.data['business_name'], 'Test Hotel') 