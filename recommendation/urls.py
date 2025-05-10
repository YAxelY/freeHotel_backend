from django.urls import path
from .views import RoomRecommendationView

urlpatterns = [
    path('rooms/<int:room_id>/', RoomRecommendationView.as_view(), name='room-recommendations'),
]