from django.urls import path
from .views import (
    HotelListCreateView,
    HotelDetailView,
    RoomListCreateView,
    RoomDetailView,
    PublishHotelView,
    PreviewHotelView,
    PublicHotelListView,
    ReviewListCreateView,
    ReviewDeleteView,
    ReviewStatsView
)

app_name = 'hotels'

urlpatterns = [
    path('', HotelListCreateView.as_view(), name='hotel-list'),
    path('public/', PublicHotelListView.as_view(), name='hotel-public-list'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),
    path('reviews/stats/', ReviewStatsView.as_view(), name='review-stats'),
    path('<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('<int:pk>/publish/', PublishHotelView.as_view(), name='hotel-publish'),
    path('<int:pk>/preview/', PreviewHotelView.as_view(), name='hotel-preview'),
    path('<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('<int:hotel_id>/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
]