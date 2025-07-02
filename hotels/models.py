from django.db import models

from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group  ,Permission

from django.utils.translation import gettext_lazy as _

from users.models import HotelOwner




class Hotel(models.Model):
    owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, related_name='hotels', null=False)
    name = models.CharField(max_length=255, default='Nouvel Hôtel')
    location = models.CharField(max_length=255, default='Paris')
    description = models.TextField(default='Description par défaut')
    rating = models.FloatField(default=0.0)
    amenities = models.JSONField(default=list)

    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    seo_settings = models.JSONField(default=dict, blank=True)
    logo_text = models.CharField(max_length=255, blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    footer_email = models.CharField(max_length=255, blank=True, null=True)
    footer_phone = models.CharField(max_length=50, blank=True, null=True)
    template_data = models.JSONField(default=dict, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # def sync_rooms_from_template_data(self):
    #     ...

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(help_text='Number of beds')
    is_available = models.BooleanField(default=True, help_text='Status: Available until booked')
    image = models.ImageField(upload_to='room_images/', blank=True, null=True, help_text='Room image file')
    # search_vector = models.JSONField(default=list, blank=True)  # We'll handle this later
    last_booking = models.DateTimeField(null=True, blank=True, help_text='Date of last reservation for this room')
    
    def update_search_vector(self):
        from recommendation.services import RecommendationEngine
        engine = RecommendationEngine()
        description = f"{self.room_type} {self.hotel.location} {self.hotel.description}"
        self.search_vector = engine.generate_embeddings(description).tolist()
        self.save()