from django.urls import path
from .views import HotelSearchView

app_name = 'search'

urlpatterns = [
    path('hotels/', HotelSearchView.as_view(), name='hotel-search'),
]