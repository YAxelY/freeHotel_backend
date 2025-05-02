from django.db import models

from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group  ,Permission

from django.utils.translation import gettext_lazy as _

from users.models import HotelOwner




class Hotel(models.Model):
    owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, related_name='hotels',null=False  )
    name = models.CharField(max_length=255, default='Nouvel Hôtel')
    location = models.CharField(max_length=255, default='Paris')
    description = models.TextField(default='Description par défaut')
    rating = models.FloatField(default=0.0)
    amenities = models.JSONField(default=list)  
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)