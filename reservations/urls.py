from django.urls import path
from .views import ReservationCreateView, ReservationListView, ReservationDetailView

app_name = 'reservations'

urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation-list'),
    path('create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
]