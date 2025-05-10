from django.db.models.signals import post_save
from django.dispatch import receiver
from hotels.models import Room

@receiver(post_save, sender=Room)
def update_room_embeddings(sender, instance, **kwargs):
    if kwargs.get('created') or kwargs.get('update_fields'):
        instance.update_search_vector()