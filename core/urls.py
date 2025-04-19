from django.urls import include, path
from .views import HotelOwnerViewSet, LoginView, LogoutView, UserMeView, UserViewSet

from .views import (
    HotelListCreateView,
    HotelDetailView,
    RoomListCreateView,
    RoomDetailView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'hotel-owners', HotelOwnerViewSet, basename='hotelowner')

from .views import CustomAuthToken

urlpatterns = [
    path('users/me/', UserMeView.as_view(), name='user-me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
        # Hotels
    path('hotels/', HotelListCreateView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    
    # Rooms
    path('hotels/<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('hotels/<int:hotel_id>/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    
    path('', include(router.urls)),
    path('users/me/', UserMeView.as_view(), name='user-me'),
] + router.urls


