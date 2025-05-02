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