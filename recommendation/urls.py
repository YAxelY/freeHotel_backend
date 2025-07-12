from django.urls import path
from .views import RoomRecommendationView, LocationHotelRecommendationView, UserRoomRecommendationView, PopularRoomRecommendationView

urlpatterns = [
    path('rooms/<int:room_id>/', RoomRecommendationView.as_view(), name='room-recommendations'),
    path('hotels/location/<str:location>/', LocationHotelRecommendationView.as_view(), name='location-hotel-recommendations'),
    path('rooms/user/', UserRoomRecommendationView.as_view(), name='user-room-recommendations'),
    path('rooms/popular/', PopularRoomRecommendationView.as_view(), name='popular-room-recommendations'),
]