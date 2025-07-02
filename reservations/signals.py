from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation
from hotels.models import Room
from django.utils import timezone

@receiver(post_save, sender=Reservation)
def set_room_unavailable_on_reservation(sender, instance, created, **kwargs):
    if created:
        room = instance.room
        room.is_available = False
        room.save()

@receiver(post_delete, sender=Reservation)
def set_room_available_on_reservation_delete(sender, instance, **kwargs):
    room = instance.room
    now = timezone.now().date()
    # Check if there are any other active reservations for this room (check_out in the future)
    active_reservations = Reservation.objects.filter(
        room=room,
        check_out__gt=now
    )
    if not active_reservations.exists():
        room.is_available = True
        room.save() 