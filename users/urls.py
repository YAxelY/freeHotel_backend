from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    HotelOwnerViewSet,
    LoginView,
    LogoutView,
    UserMeView,
    CustomAuthToken,
    HotelOwnerRegistrationView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'hotel-owners', HotelOwnerViewSet, basename='hotelowner')

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-registration'),
    path('register/hotel-owner/', HotelOwnerRegistrationView.as_view(), name='hotel-owner-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('', include(router.urls)),
]