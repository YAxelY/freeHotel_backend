from django.test import TestCase
from hotels.models import Hotel

class SearchTests(TestCase):
    def test_hotel_search(self):
        Hotel.objects.create(name="Grand Hotel", location="Paris")
        results = Hotel.objects.filter(name__icontains="Grand")
        self.assertEqual(results.count(), 1)