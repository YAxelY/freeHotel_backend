from django.urls import path
from .views import (
    HotelListCreateView,
    HotelDetailView,
    RoomListCreateView,
    RoomDetailView
)

app_name = 'hotels'

urlpatterns = [
    path('', HotelListCreateView.as_view(), name='hotel-list'),
    path('<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('<int:hotel_id>/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
]