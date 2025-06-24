from django.urls import path
from .views import (
    HotelListCreateView,
    HotelDetailView,
    RoomListCreateView,
    RoomDetailView,
    PublishHotelView,
    PreviewHotelView,
    PublicHotelListView
)

app_name = 'hotels'

urlpatterns = [
    path('', HotelListCreateView.as_view(), name='hotel-list'),
    path('public/', PublicHotelListView.as_view(), name='hotel-public-list'),
    path('<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('<int:pk>/publish/', PublishHotelView.as_view(), name='hotel-publish'),
    path('<int:pk>/preview/', PreviewHotelView.as_view(), name='hotel-preview'),
    path('<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('<int:hotel_id>/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
]