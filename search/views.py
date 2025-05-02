# search/views.py
from django_filters.rest_framework import FilterSet, CharFilter  # Import correct
from hotels.serializers import HotelSerializer
from rest_framework import generics
from hotels.models import Hotel
from django.contrib.postgres.search import SearchVector

class HotelSearchFilter(FilterSet):
    search = CharFilter(method='full_text_search')  # Plus de référence à 'filters'

    def full_text_search(self, queryset, name, value):
        return queryset.annotate(
            search=SearchVector('name', 'location', 'description')
        ).filter(search=value)

class HotelSearchView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    filterset_class = HotelSearchFilter

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from hotels.models import Hotel
from .filters import HotelSearchFilter

class HotelSearchView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer  # À créer/adapter
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelSearchFilter