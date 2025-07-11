from rest_framework import serializers
from .models import Hotel, Room, Review
from users.models import User

class RoomSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    hotel = serializers.SerializerMethodField(read_only=True)

    def get_hotel(self, obj):
        if obj.hotel:
            return {
                'id': obj.hotel.id,
                'name': obj.hotel.name,
                'logo_text': obj.hotel.logo_text,
            }
        return None

    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_number', 'room_type', 'price_per_night',
            'capacity', 'is_available', 'image', 'last_booking'
        ]
        read_only_fields = ('hotel',)
        extra_kwargs = {
            'room_number': {'required': True},
            'room_type': {'required': False},
            'capacity': {'required': True},
            'is_available': {'required': False},
            'image': {'required': False},
        }

class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'
        # Only owner, rating, and published_at are read-only; all other fields are writable
        read_only_fields = ('owner', 'rating', 'published_at')

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    profile_photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'email', 'profile_photo', 'stars', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'username', 'email', 'created_at']

    def get_username(self, obj):
        return obj.user.username or ''

    def get_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)