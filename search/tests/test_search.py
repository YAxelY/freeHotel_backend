from django.test import TestCase
from hotels.models import Hotel
from users.models import User, HotelOwner  # Ajouter les imports manquants

class SearchTests(TestCase):
    def setUp(self):
        # Créer un utilisateur et un propriétaire
        self.user = User.objects.create_user(
            email='testowner@example.com',
            password='testpass123'
        )
        self.hotel_owner = HotelOwner.objects.create(
            user=self.user,
            business_name="Test Hotels",
            contact_number="+1234567890"
        )

    def test_hotel_search(self):
        # Créer l'hôtel avec le propriétaire
        Hotel.objects.create(
            name="Grand Hotel", 
            location="Paris",
            description="Un hôtel luxueux",
            owner=self.hotel_owner  # Ajouter le propriétaire
        )
        
        # Recherche
        results = Hotel.objects.filter(name__icontains="Grand")
        self.assertEqual(results.count(), 1)