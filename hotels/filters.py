from django.db import models
from django_filters import rest_framework as filters
from .models import Hotel

class HotelFilter(filters.FilterSet):
    amenities = filters.CharFilter(method='filter_amenities')

    class Meta:
        model = Hotel
        fields = {
            'name': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
            'rating': ['gte', 'lte'],
        }
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'}
            }
        }

    def filter_amenities(self, queryset, name, value):
        return queryset.filter(amenities__contains=[value])