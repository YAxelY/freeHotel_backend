from django.db import models
from django.conf import settings
from hotels.models import Hotel
from reservations.models import Reservation

class Plan(models.Model):
    PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Pro', 'Pro'),
        ('Business', 'Business'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} (${self.price}/month)"

class HotelSubscription(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.plan.name}"

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('plan', 'Plan Subscription'),
        ('reservation', 'Reservation'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, default='pending')
    stripe_payment_id = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.payment_type} - ${self.amount}"
