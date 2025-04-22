from rest_framework import serializers
from .models import Hotel, Room

class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ('owner', 'rating')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('hotel',)
        extra_kwargs = {
            'room_number': {'required': False},
            'room_type': {'required': False},
            'capacity': {'required': False}
        }