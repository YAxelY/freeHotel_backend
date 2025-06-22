from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from reservations.models import Reservation
from users.models import User
from hotels.models import Hotel, Room, HotelOwner

class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Create hotel owner
        cls.owner = HotelOwner.objects.create(
            user=User.objects.create_user(
                email='owner@example.com',
                password='ownerpass123',
                is_hotel_owner=True
            ),
            business_name="Test Hotel"
        )
        
        # Create hotel and room
        cls.hotel = Hotel.objects.create(
            owner=cls.owner,
            name="Grand Hotel",
            location="Paris"
        )
        cls.room = Room.objects.create(
            hotel=cls.hotel,
            room_number="101",
            room_type="Deluxe",
            price_per_night=200.00,
            capacity=2
        )

    def test_create_reservation(self):
        reservation = Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=3),
            status='PENDING'
        )
        self.assertEqual(str(reservation), f"test@example.com - 101 ({date.today()} to {date.today() + timedelta(days=3)})")

    def test_invalid_dates(self):
        with self.assertRaises(ValidationError):
            reservation = Reservation(
                user=self.user,
                room=self.room,
                check_in=date.today() + timedelta(days=3),
                check_out=date.today()
            )
            reservation.full_clean()

    def test_overlapping_reservations(self):
        # Create first reservation
        Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=3),
            status='CONFIRMED'
        )
        
        # Try overlapping reservation
        with self.assertRaises(ValidationError):
            reservation = Reservation(
                user=self.user,
                room=self.room,
                check_in=date.today() + timedelta(days=1),
                check_out=date.today() + timedelta(days=4)
            )
            reservation.full_clean()



--------------------------------------------------------------

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from reservations.models import Reservation
from users.models import User
from hotels.models import Hotel, Room, HotelOwner

class ReservationViewTests(APITestCase):
    def setUp(self):
        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        
        # Create hotel owner
        self.owner = HotelOwner.objects.create(
            user=User.objects.create_user(
                email='owner@example.com',
                password='ownerpass123',
                is_hotel_owner=True
            ),
            business_name="Test Hotel"
        )
        
        # Create hotel and room
        self.hotel = Hotel.objects.create(
            owner=self.owner,
            name="Grand Hotel",
            location="Paris"
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number="101",
            room_type="Deluxe",
            price_per_night=200.00,
            capacity=2
        )
        
        # Valid reservation data
        self.valid_data = {
            "room": self.room.id,
            "check_in": date.today().isoformat(),
            "check_out": (date.today() + timedelta(days=3)).isoformat()
        }

    def test_create_reservation_unauthenticated(self):
        url = reverse('reservations:reservation-create')
        response = self.client.post(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reservation_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations:reservation-create')
        response = self.client.post(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().user, self.user)
    def test_list_reservations(self):
        # Create a reservation
        Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=2)
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations:reservation-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the paginated 'results' array
        self.assertEqual(len(response.data['results']), 1)  # Changed this line
        self.assertEqual(response.data['count'], 1)  # Add count verification
        
    def test_invalid_dates_in_request(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            "room": self.room.id,
            "check_in": (date.today() + timedelta(days=3)).isoformat(),
            "check_out": date.today().isoformat()
        }
        url = reverse('reservations:reservation-create')
        response = self.client.post(url, invalid_data)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(
            response.data['non_field_errors'][0],
            "Check-out must be after check-in"
        )

    def test_delete_reservation(self):
        reservation = Reservation.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=2)
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations:reservation-detail', kwargs={'pk': reservation.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)


-----

from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'room__hotel')
    search_fields = ('user__email', 'room__room_number')



------
from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'


----
from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from hotels.models import Room

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELED', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date")
        
        # Check for overlapping reservations
        overlapping = Reservation.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
            status__in=['PENDING', 'CONFIRMED']
        ).exclude(pk=self.pk).exists()
        
        if overlapping:
            raise ValidationError("This room is already booked for the selected dates")

    def __str__(self):
        return f"{self.user.email} - {self.room.room_number} ({self.check_in} to {self.check_out})"

    class Meta:
        ordering = ['-created_at']

------
from rest_framework import serializers

from hotels.models import Room
from .models import Reservation
from hotels.serializers import RoomSerializer

class ReservationSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        write_only=True  # Only for input, not output
    )
    room_details = RoomSerializer(source='room', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at', 'room_details')

    def validate(self, data):
        # Check if check_out is after check_in
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check-out must be after check-in")
        return data

    def create(self, validated_data):
        # Automatically set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


---
from django.urls import path
from .views import ReservationCreateView, ReservationListView, ReservationDetailView

app_name = 'reservations'

urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation-list'),
    path('create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
]

----

from rest_framework import generics, permissions
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationCreateView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # This will automatically set the user from the request
        serializer.save()

class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related('room')
    
class ReservationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
    
    

----

