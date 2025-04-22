from django.db import models  # Importer le module models de Django
from django_filters import rest_framework as filters
from hotels.models import Hotel  # Importer explicitement le modèle Hotel


class HotelSearchFilter(filters.FilterSet):
    q = filters.CharFilter(method='custom_search')

    class Meta:
        model = Hotel
        fields = ['q']

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(location__icontains=value) |
            models.Q(description__icontains=value)
        )