from django.urls import path
from .views import (
    HotelListCreateView,
    HotelDetailView,
    RoomListCreateView,
    RoomDetailView
)

urlpatterns = [
    path('hotels/', HotelListCreateView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('hotels/<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('hotels/<int:hotel_id>/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
]